# START_GLOBALS
import math

from generated.formats.nif.nimain.structs.Vector3 import Vector3
from generated.base_struct import StructMetaClass
import generated.formats.nif as NifFormat
# END_GLOBALS


class ByteVector3(Vector3, metaclass=StructMetaClass):
# START_CLASS

	@staticmethod
	def _get_filtered_attribute_list(instance, include_abstract=True):
		yield 'x', Normbyte, (0, None), (False, None)
		yield 'y', Normbyte, (0, None), (False, None)
		yield 'z', Normbyte, (0, None), (False, None)

	@staticmethod
	def validate_instance(instance, context=None, arguments=()):
		Normbyte.validate_instance(instance.x)
		Normbyte.validate_instance(instance.y)
		Normbyte.validate_instance(instance.z)
