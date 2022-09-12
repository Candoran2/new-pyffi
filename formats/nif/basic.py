from ast import literal_eval
import numpy as np
from struct import Struct

from generated.array import Array
import generated.formats.base.basic as basic
from generated.formats.nif.versions import version_from_str
from generated.io import MAX_LEN


def ve_class_from_struct(le_struct, from_value_func):
	"""Create the reading/writing class for a variable endianness struct"""

	# declare these in the local scope for faster name resolutions
	base_value = from_value_func(0)
	# these functions are used for efficient read/write of arrays
	empty = np.empty

	class ConstructedClass:

		_le_struct = le_struct
		_be_struct = Struct(le_struct.format.replace('<', '>'))

		@classmethod
		def set_struct(cls, struct):
			cls.struct = struct
			cls.pack = struct.pack
			cls.unpack = struct.unpack
			cls.size = struct.size
			cls.dtype = np.dtype(struct.format)

		@classmethod
		def update_struct(cls, context):
			if context.endian_type:
				# little endian
				cls.set_struct(cls._le_struct)
			else:
				# big endian
				cls.set_struct(cls._be_struct)

		def __new__(cls, context=None, arg=0, template=None):
			return base_value

		from_value = staticmethod(from_value_func)

		@classmethod
		def from_stream(cls, stream, context=None, arg=0, template=None):
			return cls.unpack(stream.read(cls.size))[0]

		@classmethod
		def to_stream(cls, stream, instance):
			stream.write(cls.pack(instance))

		@classmethod
		def get_size(cls, context, instance, arguments=()):
			return cls.size

		@classmethod
		def create_array(cls, shape, default=None, context=None, arg=0, template=None):
			if default:
				return np.full(shape, default, cls.dtype)
			else:
				return np.zeros(shape, cls.dtype)

		@classmethod
		def read_array(cls, stream, shape, context=None, arg=0, template=None):
			array = empty(shape, cls.dtype)
			stream.readinto(array)
			return array

		@classmethod
		def write_array(cls, stream, instance):
			# check that it is a numpy array
			if not isinstance(instance, np.ndarray):
				instance = np.array(instance, cls.dtype)
			# cast if wrong incoming dtype
			elif instance.dtype != cls.dtype:
				instance = instance.astype(cls.dtype)
			stream.write(instance.tobytes())

		@classmethod
		def functions_for_stream(cls, stream):
			# declare these in the local scope for faster name resolutions
			read = stream.read
			write = stream.write
			readinto = stream.readinto
			pack = cls.pack
			unpack = cls.unpack
			size = cls.size
			dtype = cls.dtype

			def read_value():
				return unpack(read(size))[0]

			def write_value(instance):
				write(pack(instance))

			def read_values(shape):
				array = empty(shape, dtype)
				# noinspection PyTypeChecker
				readinto(array)
				return array

			def write_values(instance):
				# check that it is a numpy array
				if not isinstance(instance, np.ndarray):
					instance = np.array(instance, dtype)
				# cast if wrong incoming dtype
				elif instance.dtype != dtype:
					instance = instance.astype(dtype)
				write(instance.tobytes())

			return read_value, write_value, read_values, write_values

		@staticmethod
		def from_xml(target, elem, prop, arguments=None):
			return literal_eval(elem.attrib[prop])

		@classmethod
		def _from_xml_array(cls, instance, elem):
			return np.fromstring(elem.text, dtype=cls.dtype, sep=" ")

		@staticmethod
		def to_xml(elem, prop, instance, arguments, debug):
			elem.attrib[prop] = str(instance)

		@staticmethod
		def _to_xml_array(instance, elem, debug):
			elem.text = " ".join([str(member) for member in instance.flat])

		@staticmethod
		def fmt_member(member, indent=0):
			lines = str(member).split("\n")
			lines_new = [lines[0], ] + ["\t" * indent + line for line in lines[1:]]
			return "\n".join(lines_new)


	ConstructedClass.set_struct(ConstructedClass._le_struct)

	return ConstructedClass


Uint64 = ve_class_from_struct(Struct("<Q"), lambda value: int(value) % 18446744073709551616)
Int64 = ve_class_from_struct(Struct("<q"), lambda value: (int(value) + 9223372036854775808) % 18446744073709551616 - 9223372036854775808)
Ulittle32 = basic.Uint
Uint = ve_class_from_struct(Struct("<I"), lambda value: int(value) % 4294967296)
Int = ve_class_from_struct(Struct("<i"), lambda value: (int(value) + 2147483648) % 4294967296 - 2147483648)
Ushort = ve_class_from_struct(Struct("<H"), lambda value: int(value) % 65536)
Short = ve_class_from_struct(Struct("<h"), lambda value: (int(value) + 32768) % 65536 - 32768)
Byte = basic.Byte
FileVersion = Ulittle32
Float = ve_class_from_struct(Struct("<f"), float)
Hfloat = ve_class_from_struct(Struct("<e"), float)

class Char:
	def __new__(cls, context=None, arg=0, template=None):
		return chr(0)

	@staticmethod
	def from_value(value):
		return chr(value)

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		return chr(Byte.from_stream(stream, context, arg, template))

	@classmethod
	def to_stream(cls, stream, instance):
		Byte.to_stream(stream, ord(instance))

	@staticmethod
	def get_size(context, instance, arguments=()):
		return 1

	@classmethod
	def _get_filtered_attribute_list_array(cls, instance):
		if isinstance(instance, str) or len(instance.shape) > 1:
			# used string to represent 1D char array
			for i in range(len(instance)):
				yield (i, cls, (0, None), (False, None))
		else:
			for i in range(instance.shape[0]):
				yield (i, Array, (0, None, instance.shape[1:], cls), (False, None))

	@staticmethod
	def fmt_member(member, indent=0):
		lines = str(member).split("\n")
		lines_new = [lines[0], ] + ["\t" * indent + line for line in lines[1:]]
		return "\n".join(lines_new)

BlockTypeIndex = Short # may need to inherit instead and be its own class

class Bool(ve_class_from_struct(Struct('<q'), lambda value: (int(value) + 2147483648) % 4294967296 - 2147483648)):
	"""A boolean; 32-bit from 4.0.0.2, and 8-bit from 4.1.0.1 on."""

	_le_byte_struct = Struct("<b")
	_be_byte_struct = Struct(">b")
	_le_int_struct = Struct("<i")
	_be_int_struct = Struct(">i")

	_byte_from_value = lambda value: (int(value) + 128) % 256 - 128
	_int_from_value = lambda value: (int(value) + 2147483648) % 4294967296 - 2147483648

	@classmethod
	def update_struct(cls, context):
		if context.version >= 0x04000002 and context.version < 0x04010001:
			# use int
			cls.from_value = staticmethod(cls._int_from_value)
			if context.endian_type:
				# little endian
				cls.set_struct(cls._le_int_struct)
			else:
				cls.set_struct(cls._be_int_struct)
		else:
			# use byte
			cls.from_value = staticmethod(cls._byte_from_value)
			if context.endian_type:
				# little endian
				cls.set_struct(cls._le_byte_struct)
			else:
				cls.set_struct(cls._be_byte_struct)


class LineString:
	"""A variable length string that ends with a newline character (0x0A)."""

	MAX_LEN = MAX_LEN

	def __new__(cls, context=None, arg=0, template=None):
		return ''

	@classmethod
	def from_stream(cls, stream, context=None, arg=0, template=None):
		"""The returned string does not include the newline."""
		val = stream.readline(cls.MAX_LEN)
		if val[-1:] != b'\n':
			if len(val) == cls.MAX_LEN:
				raise ValueError('string too long')
			else:
				raise ValueError('Reached end of file before end of {cls.__name__}')
		else:
			val = val[:-1]
		return val.decode(errors="surrogateescape")

	@staticmethod
	def to_stream(stream, instance):
		stream.write(instance.encode(errors="surrogateescape"))
		stream.write(b'\x0A')

	@staticmethod
	def get_size(context, instance, arguments=()):
		return len(instance.encode(errors="surrogateescape")) + 1

	@staticmethod
	def from_value(value, context=None, arg=0, template=None):
		return str(value)

	@staticmethod
	def fmt_member(member, indent=0):
		lines = str(member).split("\n")
		lines_new = [lines[0], ] + ["\t" * indent + line for line in lines[1:]]
		return "\n".join(lines_new)

class HeaderString(LineString):
	"""
		A variable length string that ends with a newline character (0x0A).	 The string starts as follows depending on the version:

		Version &lt;= 10.0.1.0:	 'NetImmerse File Format'
		Version &gt;= 10.1.0.0:	 'Gamebryo File Format'"""

	MAX_LEN = 64

	@staticmethod
	def version_modification_from_headerstring(s):
		s = s.rstrip()
		ver = 0
		modification = None
		if s.startswith("NetImmerse File Format, Version "):
			version_str = s[32:]
		elif s.startswith("Gamebryo File Format, Version "):
			version_str = s[30:]
		elif s.startswith("NS"):
			# neosteam
			version_str = "NS"
			modification = "neosteam"
		elif s.startswith("NDSNIF....@....@...., Version "):
			version_str = s[30:]
			modification = "ndoors"
		elif s.startswith("Joymaster HS1 Object Format - (JMI), Version "):
			version_str = s[45:]
			modification = "jmihs1"
		else:
			raise ValueError("Not a NIF file.")
		try:
			ver = version_from_str(version_str)
		except:
			raise ValueError("Nif version {version_str} not supported.")
		return ver, modification

	@classmethod
	def to_stream(cls, stream, instance=None):
		context = stream.context
		instance = cls.version_string(context)
		stream.write(instance.encode(errors="surrogateescape"))
		stream.write(b'\x0A')
	
	@staticmethod
	def version_string(context):
		"""Transforms version number into a version string.

		>>> NifFormat.HeaderString.version_string(0x03000300)
		'NetImmerse File Format, Version 3.03'
		>>> NifFormat.HeaderString.version_string(0x03010000)
		'NetImmerse File Format, Version 3.1'
		>>> NifFormat.HeaderString.version_string(0x0A000100)
		'NetImmerse File Format, Version 10.0.1.0'
		>>> NifFormat.HeaderString.version_string(0x0A010000)
		'Gamebryo File Format, Version 10.1.0.0'
		>>> NifFormat.HeaderString.version_string(0x0A010000,
		...										  modification="neosteam")
		'NS'
		>>> NifFormat.HeaderString.version_string(0x14020008,
		...										  modification="ndoors")
		'NDSNIF....@....@...., Version 20.2.0.8'
		>>> NifFormat.HeaderString.version_string(0x14030009,
		...										  modification="jmihs1")
		'Joymaster HS1 Object Format - (JMI), Version 20.3.0.9'
		"""
		version = context.version
		modification = context.modification
		if version == -1 or version is None:
			raise ValueError('No string for version %s.'%version)
		if modification == "neosteam":
			if version != 0x0A010000:
				raise ValueError("NeoSteam must have version 0x0A010000.")
			return "NS"
		elif version <= 0x0A000102:
			s = "NetImmerse"
		else:
			s = "Gamebryo"
		if version == 0x03000300:
			v = "3.03"
		elif version <= 0x03010000:
			v = "%i.%i"%((version >> 24) & 0xff, (version >> 16) & 0xff)
		else:
			v = "%i.%i.%i.%i"%((version >> 24) & 0xff, (version >> 16) & 0xff, (version >> 8) & 0xff, version & 0xff)
		if modification == "ndoors":
			return "NDSNIF....@....@...., Version %s" % v
		elif modification == "jmihs1":
			return "Joymaster HS1 Object Format - (JMI), Version %s" % v
		else:
			return "%s File Format, Version %s" % (s, v)

class Ptr(Int):
	# remove the array writing functions, because otherwise you can't assign the resolved blocks
	create_array = None
	read_array = None
	write_array = None

	@classmethod
	def to_stream(cls, stream, instance):
		if instance is None:
			index = -1
		else:
			index = stream.context._block_index_dct[instance]
		super().to_stream(stream, index)

	@staticmethod
	def fmt_member(member, indent=0):
		return f'{type(member).__name__} id: {id(member)}'

class Ref(Int):
	# remove the array writing functions, because otherwise you can't assign the resolved blocks
	create_array = None
	read_array = None
	write_array = None

	@classmethod
	def to_stream(cls, stream, instance):
		if instance is None:
			index = -1
		else:
			index = stream.context._block_index_dct[instance]
		super().to_stream(stream, index)

	@staticmethod
	def fmt_member(member, indent=0):
		return f'{type(member).__name__} id: {id(member)}'

StringOffset = Uint #although a different class, no different (except not countable)
class NiFixedString:

	def __new__(self, context, arg=0, template=None, set_default=True):
		return ''

	@staticmethod
	def from_stream(stream, context=None, arg=0, template=None):
		index = Int.from_stream(stream, context, arg, template)
		if index == -1:
			return ''
		else:
			try:
				return context.strings[index]
			except IndexError:
				raise ValueError(f'string index too large ({index})')

	@staticmethod
	def to_stream(stream, instance):
		index = -1
		for i, string in enumerate(stream.context.strings):
			if instance == string:
				index = i
				break
		Int.to_stream(stream, index)

	@staticmethod
	def get_size(context, instance, arguments=()):
		return 4

	@staticmethod
	def fmt_member(instance, indent=0):
		return repr(instance)

switchable_endianness = [Uint64, Int64, Uint, Int, Ushort, Short, Float, Hfloat, BlockTypeIndex, Bool, Ptr, Ref, StringOffset]