from importlib import import_module
from io import BytesIO
import logging
import os

from generated.formats.nif.basic import Uint, HeaderString, switchable_endianness, Ref, Ptr
from generated.formats.nif.nimain.niobjects.NiObject import NiObject
from generated.formats.nif.nimain.structs.Header import Header
from generated.formats.nif.nimain.structs.Footer import Footer
from generated.formats.nif.nimain.structs.SizedString import SizedString


def create_niobject_map():
	"""Goes through the entire directory of the nif format to find NiObjects
	and put them in a map of {name: NiObjectClass}"""
	niobject_map = {}
	current_path = os.path.dirname(os.path.abspath(__file__))
	for dirpath, dirnames, filenames in os.walk(current_path):
		if os.path.split(dirpath)[-1] != "niobjects":
			continue
		for file in filenames:
			file = os.path.splitext(file)[0]
			if file != "__init__":
				rel_path = os.path.relpath(os.path.join(dirpath, file))
				import_path = rel_path.replace(os.path.sep, ".")
				imported_module = import_module(import_path)
				file = file.upper()
				for key, value in vars(imported_module).items():
					if key.upper() == file and issubclass(value, NiObject):
						niobject_map[value.__name__] = value
	return niobject_map


# exceptions
class NifError(Exception):
	"""Standard nif exception class."""
	pass


class NifFile(Header):

	niobject_map = create_niobject_map()

	def __init__(self, context=None, arg=0, template=None, set_default=True):
		self.version = 0
		# user version and bs version will be set by init
		# use self as context
		super().__init__(self, arg, template, set_default=set_default)

	def read_blocks(self, stream):
		logger = logging.getLogger("generated.formats.nif")
		self.roots = []
		self.blocks = []
		block_num = 0
		while True:
			if self.version < 0x0303000D:
				pos = stream.tell()
				top_level_str = SizedString.from_stream(stream, self)
				if top_level_str == "Top Level Object":
					# check if this is a 'Top Level Object'
					is_root = True
				else:
					is_root = False
					stream.seek(pos)
			else:
				# signal as no root for now, roots are added when the footer
				# is read
				is_root = False

			# get block name
			if self.version >= 0x05000001:
				# note the 0xfff mask: required for the NiPhysX blocks
				block_type = self.block_types[self.block_type_index[block_num] & 0xfff]
				# handle data stream classes:
				if block_type.startswith("NiDataStream\x01"):
					block_type, data_stream_usage, data_stream_access = block_type.split("\x01")
					data_stream_usage = int(data_stream_usage)
					data_stream_access = int(data_stream_access)
				# read dummy integer
				# bhk blocks are *not* preceeded by a dummy
				if self.version <= 0x0A01006A and not block_type.startswith("bhk"):
					dummy = Uint.from_stream(stream)
					if dummy != 0:
						raise NifError(f'non-zero block tag {dummy} at {stream.tell()})')
			else:
				block_type = SizedString.from_stream(stream, self)
			# get the block index
			if self.version >= 0x0303000D:
				# for these versions the block index is simply the block number
				block_index = block_num
			else:
				# earlier versions
				# the number of blocks is not in the header
				# and a special block type string marks the end of the file
				if block_type == "End Of File": break
					# read the block index, which is probably the memory
					# location of the object when it was written to
					# memory
				else:
					block_index = Uint.from_stream(stream)
					if block_index in self._block_dct:
						raise NifError(f'duplicate block index ({block_index} at {stream.tell()})')
			# create the block
			try:
				block_class = self.niobject_map[block_type]
			except KeyError:
				raise ValueError(f"Unknown block type {block_type}.")
			logger.debug(f"Reading {block_type} block at {stream.tell()}")
			# read the block
			try:
				block = block_class.from_stream(stream, self, 0, None)
			except:
				logger.exception(f"Reading {block_class} failed")
				raise
			# complete NiDataStream data
			if block_type == "NiDataStream":
				block.usage = data_stream_usage
				block.access.populate_attribute_values(data_stream_access, self)
			self.blocks.append(block)
			# check block size
			if self.version > 0x14020007:
				logger.debug("Checking block size")
				calculated_size = block.io_size
				if calculated_size != self.block_size[block_num]:
					extra_size = self.block_size[block_num] - calculated_size
					logger.error("Block size check failed: corrupt NIF file or bad nif.xml?")
					logger.error("Skipping {extra_size} bytes in {block_type}")
					# skip bytes that were missed
					stream.seek(extra_size, 1)
			# add block to roots if flagged as such
			if is_root:
				self.roots.append(block)
			# check if we are done
			block_num += 1
			if self.version >= 0x0303000D:
				if block_num >= self.num_blocks:
					break

	def read_footer(self, stream):
		logger = logging.getLogger("generated.formats.nif")
		ftr = Footer.from_stream(stream, self)
		# check if we are at the end of the file
		if stream.read(1):
			logger.error('End of file not reached: corrupt NIF file?')

		# fix links in blocks and footer (header has no links)
		# add root objects in footer to roots list
		if self.version >= 0x0303000D:
			for root in ftr.roots:
				self.roots.append(self.blocks[root])

	@staticmethod
	def get_conditioned_attributes(struct_type, struct_instance, condition_function, arguments=()):
		for attribute in struct_type._get_filtered_attribute_list(struct_instance, *arguments[3:4]):
			if condition_function(attribute):
				yield attribute

	@classmethod
	def get_condition_attributes_recursive(cls, struct_type, struct_instance, condition_function, arguments=()):
		for attribute in struct_type._get_filtered_attribute_list(struct_instance, *arguments[3:4]):
			field_name, field_type, field_arguments = attribute[0:3]
			if condition_function(attribute):
				yield struct_type, struct_instance, attribute
			if callable(getattr(field_type, "_get_filtered_attribute_list", None)):
				yield from cls.get_condition_attributes_recursive(field_type,
												   struct_type.get_field(struct_instance, field_name),
												   condition_function,
												   field_arguments)

	def resolve_references(self):
		# go through every NiObject (and the header and footer) and replace
		# references and pointers with the actual object they're pointing to
		is_ref = lambda attribute: issubclass(attribute[1], (Ref, Ptr))
		for block in self.blocks:
			for parent_type, parent_instance, attribute in self.get_condition_attributes_recursive(type(block), block, is_ref):
				print(parent_type, attribute[0:2])
				block_index = parent_type.get_field(parent_instance, attribute[0])
				print(block_index, isinstance(block_index, int), type(block_index))
				if isinstance(block_index, int):
					print(f"can resolve ref {block_index} on {parent_type.__name__}")
				if isinstance(block_index, int):
					if block_index >= 0:
						resolved_ref = self.blocks[block_index]
					else:
						resolved_ref = None
					print(f"resolved ref {block_index} on {parent_type.__name__}")
					parent_type.set_field(parent_instance, attribute[0], resolved_ref)

	@classmethod
	def read_fields(cls, stream, instance):
		for field_name, field_type, arguments, (optional, default) in cls._get_filtered_attribute_list(instance):
			field_value = field_type.from_stream(stream, instance.context, *arguments)
			setattr(instance, field_name, field_value)
			if field_name == "header_string":
				ver, modification = HeaderString.version_modification_from_headerstring(field_value)
				instance.version = ver
				instance.modification = modification
			elif field_name == "endian_type":
				# update every basic - we now know the endianness and the version
				[basic.update_struct(instance) for basic in switchable_endianness]

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		logger = logging.getLogger("generated.formats.nif")
		logger.debug(f"Reading header at {stream.tell()}")
		cls.read_fields(stream, instance)
		logger.debug(f"Version {instance.version}")
		instance.io_size = stream.tell() - instance.io_start
		# read the separete NiObjects to build the block list
		instance.read_blocks(stream)
		# resolve references (Refs and Pointers) using the block list
		instance.resolve_references()
		# read the Footer
		instance.read_footer(stream)
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		# the context (i.e. the file) is stored on the stream
		stream.context = instance
		# create/update the block list before anything else
		# update the reverse map to allow for writing
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		# write the Footer
		Footer.to_stream(stream, instance.footer)
		return instance

	@classmethod
	def from_path(cls, filepath):
		with open(filepath, "rb") as stream:
			return cls.from_stream(stream)

	@classmethod
	def to_path(cls, filepath, instance):
		with open(filepath, "wb") as stream:
			cls.to_stream(stream, instance)

if __name__ == "__main__":
	pass