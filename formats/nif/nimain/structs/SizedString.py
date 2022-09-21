from generated.formats.nif.basic import Uint

class SizedString:

# START_CLASS

	def __new__(self, context=None, arg=0, template=None, set_default=True):
		return ''

	@staticmethod
	def from_stream(stream, context=None, arg=0, template=None):
		length = Uint.from_stream(stream)
		chars = stream.read(length)
		return chars.decode(errors="surrogateescape")

	@staticmethod
	def to_stream(stream, instance):
		Uint.to_stream(stream, len(instance))
		stream.write(instance.encode(errors="surrogateescape"))

	@staticmethod
	def get_size(context, instance, arguments=()):
		string_len = len(instance.encode(errors="surrogateescape"))
		return Uint.get_size(context, string_len) + string_len

	get_field = None
	_get_filtered_attribute_list = None

	@staticmethod
	def fmt_member(instance, indent=0):
		return repr(instance)

	@classmethod
	def validate_instance(cls, instance, context=None, arguments=()):
		assert isinstance(instance, str)
		assert len(instance) <= 4294967295
