from generated.formats.nif.basic import Uint

class SizedString:

# START_CLASS

	def __new__(self, context, arg=0, template=None, set_default=True):
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