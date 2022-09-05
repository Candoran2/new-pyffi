from importlib import import_module
from io import BytesIO
import logging
import os

from generated.formats.nif.basic import Uint, HeaderString, switchable_endianness, Ref, Ptr, NiFixedString
from generated.formats.nif.bshavok.niobjects.BhkConstraint import BhkConstraint
from generated.formats.nif.bshavok.niobjects.BhkRefObject import BhkRefObject
from generated.formats.nif.enums.DataStreamUsage import DataStreamUsage
from generated.formats.nif.bitflagss.DataStreamAccess import DataStreamAccess
from generated.formats.nif.nimain.niobjects.NiObject import NiObject
from generated.formats.nif.nimain.structs.Header import Header
from generated.formats.nif.nimain.structs.Footer import Footer
from generated.formats.nif.nimain.structs.SizedString import SizedString
from generated.formats.nif.nimain.structs.String import String


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
	"""A class to contain the actual nif data.

	Note that {blocks} are not automatically kept
	in sync with the rest of the nif data, but they are
	resynchronized when calling L{write}.

	:ivar version: The nif version.
	:type version: int
	:ivar user_version: The nif user version.
	:type user_version: int
	:ivar roots: List of root blocks.
	:type roots: list[NiObject]
	:ivar blocks: List of blocks.
	:type blocks: list[NiObject]
	:ivar modification: Neo Steam ("neosteam") or Ndoors ("ndoors") or Joymaster Interactive Howling Sword ("jmihs1") or Laxe Lore ("laxelore") style nif?
	:type modification: str
	"""
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
				if block_num >= self.num_blocks:
					break
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
				block.usage = DataStreamUsage.from_value(data_stream_usage)
				block.access = DataStreamAccess.from_value(data_stream_access)
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

	def read_footer(self, stream):
		logger = logging.getLogger("generated.formats.nif")
		ftr = Footer.from_stream(stream, self)
		# check if we are at the end of the file
		if stream.read(1):
			logger.error('End of file not reached: corrupt NIF file?')

		# add root objects in footer to roots list
		if self.version >= 0x0303000D:
			for root in ftr.roots:
				if root >= 0:
					self.roots.append(self.blocks[root])
		self.footer = ftr

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

	@classmethod
	def get_condition_values_recursive(cls, instance, condition_function, arguments=()):
		for s_type, s_inst, (f_name, f_type, arguments, _) in cls.get_condition_attributes_recursive(type(instance), instance, condition_function, arguments):
			val = s_type.get_field(s_inst, f_name)
			yield val

	@classmethod
	def get_links(cls, instance):
		condition_function = lambda x: issubclass(x[1], (Ref, Ptr))
		for val in cls.get_condition_values_recursive(instance, condition_function):
			if val is not None:
				yield val

	@classmethod
	def get_strings(cls, instance):
		"""Get all strings in the structure."""
		condition_function = lambda x: issubclass(x[1], (String, NiFixedString))
		for val in cls.get_condition_values_recursive(instance, condition_function):
			if val:
				yield val

	@classmethod
	def get_refs(cls, instance):
		condition_function = lambda x: issubclass(x[1], Ref)
		for val in cls.get_condition_values_recursive(instance, condition_function):
			if val is not None:
				yield val

	@classmethod
	def tree(cls, instance, block_type=None, follow_all=True, unique=False):
		# unique blocks: reduce this to the case of non-unique blocks
		if unique:
			block_list = []
			for block in cls.tree(instance, block_type=block_type, follow_all=follow_all, unique=False):
				if not block in block_list:
					yield block
					block_list.append(block)
		# yield instance
		if not block_type:
			yield instance
		elif isinstance(instance, block_type):
			yield instance
		elif not follow_all:
			return
		for child in cls.get_refs(instance):
			for block in cls.tree(child, block_type=block_type, follow_all=follow_all):
				yield block

	def resolve_references(self):
		# go through every NiObject and replace references and pointers with the
		# actual object they're pointing to
		is_ref = lambda attribute: issubclass(attribute[1], (Ref, Ptr))
		for block in self.blocks:
			for parent_type, parent_instance, attribute in self.get_condition_attributes_recursive(type(block), block, is_ref):
				block_index = parent_type.get_field(parent_instance, attribute[0])
				if isinstance(block_index, int):
					if block_index >= 0:
						resolved_ref = self.blocks[block_index]
					else:
						resolved_ref = None
					parent_type.set_field(parent_instance, attribute[0], resolved_ref)

	def _makeBlockList(self, root, block_index_dct, block_type_list, block_type_dct):
		"""This is a helper function for write to set up the list of all blocks,
		the block index map, and the block type map.

		:param root: The root block, whose tree is to be added to
			the block list.
		:type root: L{NifFormat.NiObject}
		:param block_index_dct: Dictionary mapping blocks in self.blocks to
			their block index.
		:type block_index_dct: dict
		:param block_type_list: List of all block types.
		:type block_type_list: list of str
		:param block_type_dct: Dictionary mapping blocks in self.blocks to
			their block type index.
		:type block_type_dct: dict
		"""
		def _blockChildBeforeParent(block):
			"""Determine whether block comes before its parent or not, depending
			on the block type.

			@todo: Move to the L{NifFormat.Data} class.

			:param block: The block to test.
			:type block: L{NifFormat.NiObject}
			:return: ``True`` if child should come first, ``False`` otherwise.
			"""
			return (isinstance(block, BhkRefObject)
					and not isinstance(block, BhkConstraint))

		# block already listed? if so, return
		if root in self.blocks:
			return

		# add block type to block type dictionary
		block_type = type(root).__name__
		# special case: NiDataStream stores part of data in block type list
		if block_type == "NiDataStream":
			block_type = "NiDataStream\x01{int(root.usage)}\x01%{int(root.access)}"
		try:
			block_type_dct[root] = block_type_list.index(block_type)
		except ValueError:
			block_type_dct[root] = len(block_type_list)
			block_type_list.append(block_type)

		# special case: add bhkConstraint entities before bhkConstraint
		# (these are actually links, not refs)
		if isinstance(root, BhkConstraint):
			for entity in root.entities:
				if entity is not None:
					self._makeBlockList(entity, block_index_dct, block_type_list, block_type_dct)

		children_left = []
		# add children that come before the block
		# store any remaining children in children_left (processed later)
		for child in self.get_refs(root):
			if _blockChildBeforeParent(child):
				self._makeBlockList(child, block_index_dct, block_type_list, block_type_dct)
			else:
				children_left.append(child)

		# add the block
		if self.version >= 0x030300D:
			block_index_dct[root] = len(self.blocks)
		else:
			block_index_dct[root] = id(root)
		self.blocks.append(root)

		for child in children_left:
			self._makeBlockList(child, block_index_dct, block_type_list, block_type_dct)

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
		logger = logging.getLogger("generated.formats.nif")
		# the context (i.e. the file) is stored on the stream
		stream.context = instance
		# set up index and type dictionary
		instance.blocks = [] # list of all blocks to be written
		instance._block_index_dct = {} # maps block to block index
		block_type_list = [] # list of all block type strings
		block_type_dct = {} # maps block to block type string index
		instance._string_list = []
		# create/update the block list before anything else
		for root in instance.roots:
			instance._makeBlockList(root, instance._block_index_dct, block_type_list, block_type_dct)
			for block in cls.tree(root):
				instance._string_list.extend(cls.get_strings(block))
		instance._string_list = list(set(instance._string_list))  # ensure unique elements

		instance.num_blocks = len(instance.blocks)
		instance.num_block_types = len(block_type_list)
		instance.block_types[:] = block_type_list
		instance.block_type_index[:] = [block_type_dct[block] for block in instance.blocks]
		instance.num_strings = len(instance._string_list)
		if instance._string_list:
			instance.max_string_length = max([len(s) for s in instance._string_list])
		else:
			instance.max_string_length = 0
		instance.strings[:] = instance._string_list
		instance.block_size[:] = [type(block).get_size(instance, block) for block in instance.blocks]

		# write the header (instance)
		logger.debug("Writing header")
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start

		# write the blocks
		for block in instance.blocks:
			# signal top level object if block is a root object
			if instance.version < 0x0303000D and block in instance.roots:
				SizedString.to_stream(stream, "Top Level Object")
			if instance.version >= 0x05000001:
				if instance.version <= 0x0A01006A:
					# write zero dummy separator
					Uint.to_stream(stream, 0)
			else:
				# write block type string
				assert(block_type_list[block_type_dct[block]] == type(block).__name__)
				SizedString.to_stream(stream, type(block).__name__)
			# write block index
			logger.debug(f"Writing {type(block).__name__} block")
			if instance.version < 0x0303000D:
				Uint.to_stream(stream, instance._block_index_dct[block]) # original pyffi code had Int
			# write block
			type(block).to_stream(stream, block)
		if instance.version < 0x0303000D:
			SizedString.to_stream(stream, "End Of File")

		# write the Footer
		ftr = instance.footer
		ftr.num_roots = len(instance.roots)
		ftr.roots[:] = instance.roots
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