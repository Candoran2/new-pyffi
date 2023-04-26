# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS
from generated.base_struct import BaseStruct
from generated.formats.nif.imports import name_type_map


class ExportString(BaseStruct):


# START_CLASS

	def __new__(self, context, arg=0, template=None, set_default=True):
		return ''

	@staticmethod
	def from_stream(stream, context=None, arg=0, template=None):
		length = name_type_map["Byte"].from_stream(stream)
		chars = stream.read(length)[:-1]
		return NifFormat.safe_decode(chars)

	@staticmethod
	def to_stream(instance, stream, context, arg=0, template=None):
		instance = instance + '\x00'
		encoded_instance = NifFormat.encode(instance)
		length = len(encoded_instance)
		name_type_map["Byte"].to_stream(length, stream, context)
		stream.write(encoded_instance)

	@staticmethod
	def get_size(instance, context, arg=0, template=None):
		string_len = len(NifFormat.encode(instance)) + 1
		return name_type_map["Byte"].get_size(string_len, context) + string_len

	@classmethod
	def validate_instance(cls, instance, context=None, arg=0, template=None):
		assert isinstance(instance, str), f'{instance} is not a string'
		name_type_map["Byte"].validate_instance(len(NifFormat.encode(instance + '\x00')), context)

	get_field = None
	_get_filtered_attribute_list = None

	@staticmethod
	def from_value(value):
		return str(value)
