from generated.formats.nif.basic import Uint
from generated.formats.nif.nimain.structs.SizedString import SizedString

class StringPalette:

# START_CLASS


	def __new__(self, context=None, arg=0, template=None, set_default=True):
		return ['']

	@staticmethod
	def from_stream(stream, context=None, arg=0, template=None):
		palette = SizedString.from_stream(stream, context)
		# need to consume length from the stream
		length = Uint.from_stream(stream, context)
		# palette are \x00 terminated strings, so the last one should be empty
		palette = palette.split("\x00")[:-1]
		return palette

	@staticmethod
	def to_stream(stream, instance):
		palette = "\x00".join(instance) + "\x00"
		SizedString.to_stream(stream, palette)
		Uint.to_stream(len(SizedString))

	@staticmethod
	def get_size(context, instance, arguments=()):
		palette_string_len = sum([len(string.encode(errors="surrogateescape")) for string in instance]) + len(instance)
		return Uint.get_size(context, palette_string_len) + palette_string_len + Uint.get_size(context, palette_string_len)

	get_field = None
	_get_filtered_attribute_list = None

	@staticmethod
	def fmt_member(instance, indent=0):
		return repr(instance)

