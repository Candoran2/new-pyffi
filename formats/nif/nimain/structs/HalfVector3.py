# START_GLOBALS
import math

from generated.formats.nif.nimain.structs.Vector3 import Vector3
from generated.base_struct import StructMetaClass
import generated.formats.nif as NifFormat
# END_GLOBALS


class HalfVector3(Vector3, metaclass=StructMetaClass):
# START_CLASS

	@staticmethod
	def _get_filtered_attribute_list(instance, include_abstract=True):
		yield 'x', name_type_map["Hfloat"], (0, None), (False, None)
		yield 'y', name_type_map["Hfloat"], (0, None), (False, None)
		yield 'z', name_type_map["Hfloat"], (0, None), (False, None)

	@staticmethod
	def validate_instance(instance, context=None, arg=0, template=None):
		name_type_map["Hfloat"].validate_instance(instance.x)
		name_type_map["Hfloat"].validate_instance(instance.y)
		name_type_map["Hfloat"].validate_instance(instance.z)
