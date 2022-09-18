from importlib import import_module
from io import BytesIO
import logging
import os
import re

from generated.formats.nif.basic import Uint, FileVersion, Ulittle32, LineString, HeaderString, switchable_endianness, Ref, Ptr, NiFixedString
from generated.formats.nif.bsmain.structs.BSStreamHeader import BSStreamHeader
from generated.formats.nif.enums.DataStreamUsage import DataStreamUsage
from generated.formats.nif.enums.EndianType import EndianType
from generated.formats.nif.bitflagss.DataStreamAccess import DataStreamAccess
from generated.formats.nif.nimain.niobjects.NiObject import NiObject
from generated.formats.nif.nimain.structs.Header import Header
from generated.formats.nif.nimain.structs.Footer import Footer
from generated.formats.nif.nimain.structs.SizedString import SizedString
from generated.formats.nif.nimain.structs.String import String
from generated.formats.nif.versions import has_bs_ver


class _attr_dict(dict):

	def __getattr__(self, key):
		return self[key]


def create_niclasses_map():
	"""Goes through the entire directory of the nif format to find all defined
	classes and put them in a map of {local_name: class}"""
	niclasses_map = _attr_dict()
	current_path = os.path.dirname(os.path.abspath(__file__))
	for dirpath, dirnames, filenames in os.walk(current_path):
		if os.path.split(dirpath)[-1] not in ("niobjects", "structs", "bitfields", "bitflagss", "enums"):
			continue
		for file in filenames:
			file, extension = os.path.splitext(file)
			if file != "__init__" and extension == ".py":
				rel_path = os.path.relpath(os.path.join(dirpath, file), start=current_path)
				import_path = f".{rel_path.replace(os.path.sep, '.')}"
				imported_module = import_module(import_path, __name__)
				file = file.upper()
				for key, value in vars(imported_module).items():
					if key.upper() == file:
						niclasses_map[key] = value
	return niclasses_map


def get_conditioned_attributes(struct_type, struct_instance, condition_function, arguments=(), include_abstract=True):
	for attribute in struct_type._get_filtered_attribute_list(struct_instance, *arguments[3:4], include_abstract):
		if condition_function(attribute):
			yield attribute


def get_condition_attributes_recursive(struct_type, struct_instance, condition_function, arguments=(), include_abstract=True):
	for attribute in struct_type._get_filtered_attribute_list(struct_instance, *arguments[3:4], include_abstract):
		field_name, field_type, field_arguments = attribute[0:3]
		if condition_function(attribute):
			yield struct_type, struct_instance, attribute
		if callable(getattr(field_type, "_get_filtered_attribute_list", None)):
			yield from get_condition_attributes_recursive(field_type,
											   struct_type.get_field(struct_instance, field_name),
											   condition_function,
											   field_arguments,
											   include_abstract)


def get_condition_values_recursive(instance, condition_function, arguments=(), include_abstract=True):
	for s_type, s_inst, (f_name, f_type, arguments, _) in get_condition_attributes_recursive(type(instance), instance, condition_function, arguments, include_abstract):
		val = s_type.get_field(s_inst, f_name)
		yield val

# filter for recognizing NIF files by extension
# .kf are NIF files containing keyframes
# .kfa are NIF files containing keyframes in DAoC style
# .nifcache are Empire Earth II NIF files
# .texcache are Empire Earth II/III packed texture NIF files
# .pcpatch are Empire Earth II/III packed texture NIF files
# .item are Divinity 2 NIF files
# .nft are Bully SE NIF files (containing textures)
# .nif_wii are Epic Mickey NIF files
RE_FILENAME = re.compile(r'^.*\.(nif|kf|kfa|nifcache|jmi|texcache|pcpatch|nft|item|nif_wii)$', re.IGNORECASE)
# archives
ARCHIVE_CLASSES = [] # link to the actual bsa format once done
# used for comparing floats
EPSILON = 0.0001

classes = create_niclasses_map()
niobject_map = {niclass.__name__: niclass for niclass in classes.values() if issubclass(niclass, NiObject)}


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

	def __init__(self, context=None, arg=0, template=None, set_default=True):
		# user version and bs version will be set by init
		# use self as context
		super().__init__(self, arg, template, set_default=set_default)
		self.roots = []
		self.blocks = []
		self.modification = None

	@staticmethod
	def inspect_version_only(stream):
		pos = stream.tell()
		try:
			header_string = HeaderString.from_stream(stream)
			h_ver, modification = HeaderString.version_modification_from_headerstring(header_string)
			if h_ver <= 0x03010000:
				LineString.from_stream(stream)
			ver_int = FileVersion.from_stream(stream)
			# special case for Laxe Lore
			if h_ver == 0x14000004 and ver_int == 0x5A000004:
				modification = "laxelore"
			# neosteam and ndoors have a special version integer
			elif (not modification) or modification == "jmihs1":
				 if ver_int != h_ver:
					 raise ValueError(f"Corrupted NIF file: header version string in {header_string} does not "
					   f"correspond with header version field {ver_int}")
			elif modification == "neosteam":
				if ver_int != 0x08F35232:
					raise ValueError("Corrupted NIF file: invalid NeoSteam version.")
			elif modification == "ndoors":
				if ver_int != 0x73615F67:
					raise ValueError("Corrupted NIF file: invalid Ndoors version.")
			# read EndianType to advance stream
			if ver_int >= 0x14000004:
				EndianType.from_stream(stream)
			user = 0
			bsver = 0
			if ver_int >= 0x0A010000:
				user = Ulittle32.from_stream(stream)
				# only need to set bsver if Bethesda
				if has_bs_ver(ver_int, user):
					# read num_blocks
					Ulittle32.from_stream(stream)
					bsver = Ulittle32.from_stream(stream)
			return modification, (ver_int, user, bsver)
		finally:
			stream.seek(pos)

	@classmethod
	def from_version(cls, version=0x04000002, user_version=0, user_version_2=0):
		"""Initialize nif data. By default, this creates an empty
		nif document of the given version and user version.

		:param version: The version.
		:type version: int
		:param user_version: The user version.
		:type user_version: int
		"""
		instance = cls()
		instance.version = version
		instance.user_version = user_version
		for f_name, f_type, arguments, (optional, default) in cls._get_filtered_attribute_list(instance):
			if f_name == "version":
				continue
			elif f_name == "user_version":
				continue
			elif f_name == "bs_header":
				field_value = BSStreamHeader.from_bs_version(instance, user_version_2)
			else:
				if default is None:
					field_value = f_type(instance, *arguments)
				else:
					field_value = f_type.from_value(*arguments[2:4], default)
			setattr(instance, f_name, field_value)
		return instance

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
				block_class = niobject_map[block_type]
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

	# GlobalNode
	def get_global_child_nodes(self, edge_filter=()):
		return (root for root in self.roots)

	@classmethod
	def get_strings(cls, instance):
		"""Get all strings in the structure."""
		condition_function = lambda x: issubclass(x[1], (String, NiFixedString))
		for val in get_condition_values_recursive(instance, condition_function):
			if val:
				yield val

	@classmethod
	def get_recursive_strings(cls, instance):
		"""Get all strings in the entire tree"""
		condition_function = lambda x: issubclass(x[1], (String, NiFixedString, Ref))
		for s_type, s_inst, (f_name, f_type, arguments, _) in get_condition_attributes_recursive(type(instance), instance, condition_function):
			value = s_type.get_field(s_inst, f_name)
			if issubclass(f_type, Ref):
				if value is not None:
					yield from cls.get_recursive_strings(value)
			else:
				# must be a string type
				if value:
					yield value

	def resolve_references(self):
		# go through every NiObject and replace references and pointers with the
		# actual object they're pointing to
		is_ref = lambda attribute: issubclass(attribute[1], (Ref, Ptr))
		for block in self.blocks:
			for parent_type, parent_instance, attribute in get_condition_attributes_recursive(type(block), block, is_ref):
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
			return (isinstance(block, niobject_map["bhkRefObject"])
					and not isinstance(block, niobject_map["bhkConstraint"]))

		# block already listed? if so, return
		if root in self.blocks:
			return

		# add block type to block type dictionary
		block_type = type(root).__name__
		# special case: NiDataStream stores part of data in block type list
		if block_type == "NiDataStream":
			block_type = f"NiDataStream\x01{int(root.usage)}\x01{int(root.access)}"
		try:
			block_type_dct[root] = block_type_list.index(block_type)
		except ValueError:
			block_type_dct[root] = len(block_type_list)
			block_type_list.append(block_type)

		# special case: add bhkConstraint entities before bhkConstraint
		# (these are actually links, not refs)
		if isinstance(root, niobject_map["bhkConstraint"]):
			for entity in root.entities:
				if entity is not None:
					self._makeBlockList(entity, block_index_dct, block_type_list, block_type_dct)

		children_left = []
		# add children that come before the block
		# store any remaining children in children_left (processed later)
		for child in root.get_refs():
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
		for field_name, field_type, arguments, (optional, default) in cls._get_filtered_attribute_list(instance, include_abstract=False):
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
			instance._string_list.extend(cls.get_recursive_strings(root))
# 			recursive strings (at least for test maplestory 2 (30.2.0.3) nif) is more true to base game order
# 			than get_strings per block
# 			for block in cls.tree(root):
# 				instance._string_list.extend(cls.get_strings(block))
		instance._string_list = list({string: None for string in instance._string_list})  # ensure unique elements

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

		# update the basics before doing any writing
		[basic.update_struct(instance) for basic in switchable_endianness]
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
		ftr = Footer(instance)
		ftr.num_roots = len(instance.roots)
		ftr.roots[:] = instance.roots
		Footer.to_stream(stream, ftr)
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