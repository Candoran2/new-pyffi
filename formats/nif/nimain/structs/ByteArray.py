from generated.array import Array
from generated.formats.nif.imports import name_type_map

class ByteArray:
# START_CLASS

	def __new__(self, context=None, arg=0, template=None, set_default=True):
		data_size = name_type_map["Uint"](context, 0, None)
		return b'\x00' * data_size

	@staticmethod
	def from_stream(stream, context=None, arg=0, template=None):
		data_size = name_type_map["Uint"].from_stream(stream)
		return stream.read(data_size)

	@staticmethod
	def to_stream(instance, stream, context, arg=0, template=None):
		data_size = len(instance)
		name_type_map["Uint"].to_stream(data_size, stream, context, 0, None)
		stream.write(instance)

	@staticmethod
	def get_size(instance, context, arg=0, template=None):
		data_size = len(instance)
		return name_type_map["Uint"].get_size(data_size, context, 0, None) + data_size

	get_field = None
	_get_filtered_attribute_list = None

	@staticmethod
	def fmt_member(instance, indent=0):
		return repr(instance)

	@classmethod
	def validate_instance(cls, instance, context=None, arg=0, template=None):
		data_size = len(instance)
		name_type_map["Uint"].validate_instance(data_size, context, 0, None)
		assert isinstance(instance, (bytes, bytearray)), f'{instance} is not a byte or bytearray'