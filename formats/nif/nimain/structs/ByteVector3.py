# START_GLOBALS
import math

from generated.formats.nif.nimain.structs.Vector3 import Vector3
from generated.base_struct import StructMetaClass
import generated.formats.nif as NifFormat
# END_GLOBALS


class ByteVector3(Vector3, metaclass=StructMetaClass):
# START_CLASS

	def __init__(self, context=None, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.x = 0
		self.y = 0
		self.z = 0

	@staticmethod
	def _get_filtered_attribute_list(instance, include_abstract=True):
		yield 'x', Byte, (0, None), (False, None)
		yield 'y', Byte, (0, None), (False, None)
		yield 'z', Byte, (0, None), (False, None)

	@staticmethod
	def validate_instance(instance, context=None, arguments=()):
		Byte.validate_instance(instance.x)
		Byte.validate_instance(instance.y)
		Byte.validate_instance(instance.z)
