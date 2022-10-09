# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS
from generated.base_struct import BaseStruct
from generated.formats.nif.basic import Byte


class ExportString(BaseStruct):


# START_CLASS

	def __new__(self, context, arg=0, template=None, set_default=True):
		return ''

	@staticmethod
	def from_stream(stream, context=None, arg=0, template=None):
		length = Byte.from_stream(stream)
		chars = stream.read(length)[:-1]
		return NifFormat.safe_decode(chars)

	@staticmethod
	def to_stream(stream, instance):
		instance = instance + '\x00'
		encoded_instance = NifFormat.encode(instance)
		length = len(encoded_instance)
		Byte.to_stream(stream, length)
		stream.write(encoded_instance)

	@staticmethod
	def get_size(context, instance, arguments=()):
		string_len = len(NifFormat.encode(instance)) + 1
		return Byte.get_size(context, string_len) + string_len

	@classmethod
	def validate_instance(cls, instance, context=None, arguments=()):
		assert isinstance(instance, str)
		assert len(NifFormat.encode(instance + '\x00')) <= 255

	get_field = None
	_get_filtered_attribute_list = None

	@staticmethod
	def from_value(value):
		return str(value)
