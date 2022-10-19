# START_GLOBALS
import numpy as np

from generated.base_struct import BaseStruct
import generated.formats.nif.basic as NifBasic
import generated.formats.base.basic as BaseBasic
from generated.formats.nif.enums.ComponentType import ComponentType


class UnormByte(NifBasic.UNormClass):

	storage = NifBasic.Byte

	@staticmethod
	def from_function(instance):
		return instance / 255.0

	@staticmethod
	def to_function(instance):
		return np.round(instance * 255)
# END_GLOBALS

class ComponentFormat:

# START_CLASS

	@classmethod
	def struct_for_type(cls, format_type):
		if format_type == ComponentType.F_UNKNOWN:
			# raw bytes
			return NifBasic.Byte
		elif ComponentType.F_INT8_1 <= format_type <= ComponentType.F_INT8_4:
			# signed byte
			return BaseBasic.Byte
		elif ComponentType.F_UINT8_1 <= format_type <= ComponentType.F_UINT8_4:
			# unsigned byte
			return NifBasic.Byte
		elif ComponentType.F_NORMINT8_1 <= format_type <= ComponentType.F_NORMINT8_4:
			# normalized signed byte
			return NifBasic.Normbyte
		elif ComponentType.F_NORMUINT8_1 <= format_type <= ComponentType.F_NORMUINT8_4:
			# normalized unsigned byte
			return UnormByte
		elif ComponentType.F_INT16_1 <= format_type <= ComponentType.F_INT16_4:
			# signed short
			return NifBasic.Short
		elif ComponentType.F_UINT16_1 <= format_type <= ComponentType.F_UINT16_4:
			# unsigned short
			return NifBasic.Ushort
		elif ComponentType.F_NORMINT16_1 <= format_type <= ComponentType.F_NORMINT16_4:
			# normalized signed short
			raise NotImplementedError
		elif ComponentType.F_NORMUINT16_1 <= format_type <= ComponentType.F_NORMUINT16_4:
			# normalized unsigned short
			raise NotImplementedError
		elif ComponentType.F_INT32_1 <= format_type <= ComponentType.F_INT32_4:
			# signed int32
			return NifBasic.Int
		elif ComponentType.F_UINT32_1 <= format_type <= ComponentType.F_UINT32_4:
			# unsigned int32
			return NifBasic.Uint
		elif ComponentType.F_NORMINT32_1 <= format_type <= ComponentType.F_NORMINT32_4:
			# normalized signed int32
			raise NotImplementedError
		elif ComponentType.F_NORMUINT32_1 <= format_type <= ComponentType.F_NORMUINT32_4:
			# normalized unsigned int32
			raise NotImplementedError
		elif ComponentType.F_FLOAT16_1 <= format_type <= ComponentType.F_FLOAT16_4:
			# hfloat
			return NifBasic.Hfloat
		elif ComponentType.F_FLOAT32_1 <= format_type <= ComponentType.F_FLOAT32_4:
			# float32
			return NifBasic.Float
		elif format_type == ComponentType.F_UINT_10_10_10_L1:
			raise NotImplementedError
		elif format_type == ComponentType.F_NORMINT_10_10_10_L1:
			raise NotImplementedError
		elif format_type == ComponentType.F_NORMINT_11_11_10:
			raise NotImplementedError
		elif format_type == ComponentType.F_NORMUINT8_4_BGRA:
			# like color4 but switched around - individual components are unormbyte
			return UnormByte
		elif format_type == ComponentType.F_NORMINT_10_10_10_2:
			raise NotImplementedError
		elif format_type == ComponentType.F_UINT_10_10_10_2:
			raise NotImplementedError
		elif format_type == ComponentType.F_UNKNOWN_20240:
			# some kind of unknown two-byte-wide component type
			raise NotImplementedError
		raise NotImplementedError

	@classmethod
	def get_component_size(cls, format_description):
		return format_description.element_width * format_description.num_elements

	@classmethod
	def struct_from_format(cls, format_description):
		# create a struct representing the componentformat description
		element_type = cls.struct_for_type(format_description.type)
		if format_description.num_elements <= 1:
			return element_type
		else:
			field_names = [f"c{i}" for i in range(format_description.num_elements)]


			class created_struct(BaseStruct):

				__name__  = format_description.type.name

				_attribute_list = [(f_name, element_type, (0, None), (False, None), None) for f_name in field_names]

				@staticmethod
				def _get_filtered_attribute_list(instance, include_abstract=True):
					for f_name in field_names:
						yield f_name, element_type, (0, None), (False, None)


			return created_struct