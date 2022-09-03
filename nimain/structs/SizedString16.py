from generated.formats.nif.basic import Ushort

class SizedString16:

# START_CLASS

	def __new__(self, context, arg=0, template=None, set_default=True):
		return ''

	@staticmethod
	def from_stream(stream, context=None, arg=0, template=None):
		length = Ushort.from_stream(stream)
		chars = stream.read(length)
		return chars.decode(errors="surrogateescape")

	@staticmethod
	def to_stream(stream, instance):
		Ushort.to_stream(stream, len(instance))
		stream.write(instance.encode(errors="surrogateescape"))

	@staticmethod
	def get_field(instance, key):
		if key == "length":
			return len(instance)
		elif key == "chars":
			return instance
