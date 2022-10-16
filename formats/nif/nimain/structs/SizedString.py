# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS
from generated.formats.nif.basic import Uint

class SizedString:

# START_CLASS

	def __new__(self, context=None, arg=0, template=None, set_default=True):
		return ''

	@staticmethod
	def from_stream(stream, context=None, arg=0, template=None):
		length = Uint.from_stream(stream)
		chars = stream.read(length)
		return NifFormat.safe_decode(chars)

	@staticmethod
	def to_stream(instance, stream, context, arg=0, template=None):
		encoded_instance = NifFormat.encode(instance)
		Uint.to_stream(len(encoded_instance), stream, context)
		stream.write(encoded_instance)

	@staticmethod
	def get_size(instance, context, arg=0, template=None):
		string_len = len(NifFormat.encode(instance))
		return Uint.get_size(string_len, context) + string_len

	get_field = None
	_get_filtered_attribute_list = None

	@staticmethod
	def fmt_member(instance, indent=0):
		return repr(instance)

	@classmethod
	def validate_instance(cls, instance, context=None, arg=0, template=None):
		assert isinstance(instance, str)
		assert len(NifFormat.encode(instance)) <= 4294967295

	@staticmethod
	def from_value(value):
		return str(value)
