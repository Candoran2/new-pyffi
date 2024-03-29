# START_GLOBALS
import numpy as np

from generated.base_struct import BaseStruct
from generated.bitfield import BasicBitfield, BitfieldMember
import generated.formats.nif.basic as NifBasic
import generated.formats.base.basic as BaseBasic


class NormByte(NifBasic.NormClass):

	storage = BaseBasic.Byte

	@staticmethod
	def from_function(instance):
        # function based on Epic Mickey AL_Interior_BlackBox01.nif_wii
        # best guess - however, is not necessarily the only correct function
		return (2 * instance + 1) / 255

	@staticmethod
	def to_function(instance):
		return np.round(((255 * instance) - 1) / 2)


class UNormByte(NifBasic.UNormClass):

	storage = NifBasic.Byte

	@staticmethod
	def from_function(instance):
		return instance / 255.0

	@staticmethod
	def to_function(instance):
		return np.round(instance * 255)


class NormShort(NifBasic.NormClass):

	storage = NifBasic.Short

	@staticmethod
	def from_function(instance):
		return (2 * instance + 1) / 65535

	@staticmethod
	def to_function(instance):
		return np.round(((65535 * instance) - 1) / 2)


class UNormShort(NifBasic.UNormClass):

	storage = NifBasic.Ushort

	@staticmethod
	def from_function(instance):
		return instance / 65535.0

	@staticmethod
	def to_function(instance):
		return np.round(instance * 65535.0)


class NormInt(NifBasic.NormClass):

	storage = NifBasic.Int

	@staticmethod
	def from_function(instance):
		return (2 * instance + 1) / 4294967295

	@staticmethod
	def to_function(instance):
		return np.round(((4294967295 * instance) - 1) / 2)


class UNormInt(NifBasic.UNormClass):

	storage = NifBasic.Uint

	@staticmethod
	def from_function(instance):
		return instance / 4294967295.0

	@staticmethod
	def to_function(instance):
		return np.round(instance * 4294967295.0)


class Format40(NifBasic.UNormClass):
	"""Seems to be shorts divided by 1023, based on EM UV map"""

	storage = NifBasic.Short

	@staticmethod
	def from_value(value):
		return min(max(0.0, value), 64.06158357771261)

	@classmethod
	def validate_instance(cls, instance, context=None, arg=0, template=None):
		assert instance >= 0.0
		assert instance <= 64.06158357771261

	@staticmethod
	def from_function(instance):
		return instance / 1023.0

	@staticmethod
	def to_function(instance):
		return np.round(instance * 1023.0)


class Bitfield39(BasicBitfield):
	c1 = BitfieldMember(pos=0, mask=0x3FF, return_type=int)
	c2 = BitfieldMember(pos=10, mask=0xFFC00, return_type=int)
	c3 = BitfieldMember(pos=20, mask=0x3FF00000, return_type=int)
# END_GLOBALS

class ComponentFormat:

# START_CLASS

	_non_members_ = ["_storage", "struct_map"]

	struct_map = {}

	@classmethod
	def struct_for_type(cls, format_type):
		# note: does not agree with noesis
		if format_type == cls.F_UNKNOWN.type_id:
			# raw bytes
			return NifBasic.Byte
		elif cls.F_INT8_1.type_id <= format_type <= cls.F_INT8_4.type_id:
			# signed byte
			return BaseBasic.Byte
		elif cls.F_UINT8_1.type_id <= format_type <= cls.F_UINT8_4.type_id:
			# unsigned byte
			return NifBasic.Byte
		elif cls.F_NORMINT8_1.type_id <= format_type <= cls.F_NORMINT8_4.type_id:
			# normalized signed byte
			return NormByte
		elif cls.F_NORMUINT8_1.type_id <= format_type <= cls.F_NORMUINT8_4.type_id:
			# normalized unsigned byte
			return UNormByte
		elif cls.F_INT16_1.type_id <= format_type <= cls.F_INT16_4.type_id:
			# signed short
			return NifBasic.Short
		elif cls.F_UINT16_1.type_id <= format_type <= cls.F_UINT16_4.type_id:
			# unsigned short
			return NifBasic.Ushort
		elif cls.F_NORMINT16_1.type_id <= format_type <= cls.F_NORMINT16_4.type_id:
			# normalized signed short
			return NormShort
		elif cls.F_NORMUINT16_1.type_id <= format_type <= cls.F_NORMUINT16_4.type_id:
			# normalized unsigned short
			return UNormShort
		elif cls.F_INT32_1.type_id <= format_type <= cls.F_INT32_4.type_id:
			# signed int32
			return NifBasic.Int
		elif cls.F_UINT32_1.type_id <= format_type <= cls.F_UINT32_4.type_id:
			# unsigned int32
			return NifBasic.Uint
		elif cls.F_NORMINT32_1.type_id <= format_type <= cls.F_NORMINT32_4.type_id:
			# normalized signed int32
			return NormInt
		elif cls.F_NORMUINT32_1.type_id <= format_type <= cls.F_NORMUINT32_4.type_id:
			# normalized unsigned int32
			return UNormInt
		elif cls.F_FLOAT16_1.type_id <= format_type <= cls.F_FLOAT16_4.type_id:
			# hfloat
			return NifBasic.Hfloat
		elif cls.F_FLOAT32_1.type_id <= format_type <= cls.F_FLOAT32_4.type_id:
			# float32
			return NifBasic.Float
		elif format_type == cls.F_UINT_10_10_10_L1.type_id:
			return Bitfield39
		elif format_type == cls.F_NORMINT_10_10_10_L1.type_id:
			# return simple int for now
			return NifBasic.Int
		elif format_type == cls.F_NORMINT_11_11_10.type_id:
			# return simple int for now
			return NifBasic.Int
		elif format_type == cls.F_NORMUINT8_4_BGRA.type_id:
			# like color4 but switched around - individual components are unormbyte
			return UNormByte
		elif format_type == cls.F_NORMINT_10_10_10_2.type_id:
			# return simple int for now
			return NifBasic.Int
		elif format_type == cls.F_UINT_10_10_10_2.type_id:
			# return simple int for now
			return NifBasic.Int
		elif format_type == cls.F_UNKNOWN_20240.type_id:
			# non-standard format guess based on Epic Mickey UV map.
			return Format40
		raise NotImplementedError

	@property
	def type_id(self):
		return self & 0xFF

	@property
	def element_width(self):
		return (self & 0x0000FF00) >> 8

	@property
	def num_elements(self):
		return (self & 0x00FF0000) >> 16

	@classmethod
	def get_component_size(cls, format_description):
		return format_description.element_width * format_description.num_elements

	@classmethod
	def create_struct_from_format(cls, format_description):
		# create a struct representing the componentformat description
		element_type = cls.struct_for_type(format_description & 0xFF)
		if format_description.num_elements <= 1:
			return element_type
		else:
			field_names = [f"c{i}" for i in range(format_description.num_elements)]


			class created_struct(BaseStruct):

				__name__  = format_description.name

				@staticmethod
				def _get_attribute_list():
					for f_name in field_names:
						yield (f_name, element_type, (0, None), (False, None), (None, None))

				@staticmethod
				def _get_filtered_attribute_list(instance, include_abstract=True):
					for f_name in field_names:
						yield f_name, element_type, (0, None), (False, None)

			created_struct.init_attributes()

			return created_struct

	@classmethod
	def struct_for_format(cls, format_description):
		if format_description in cls.struct_map:
			return cls.struct_map[format_description]
		else:
			created_struct = cls.create_struct_from_format(format_description)
			cls.struct_map[format_description] = created_struct
			return created_struct