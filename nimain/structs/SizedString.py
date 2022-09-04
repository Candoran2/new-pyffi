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

	@staticmethod
	def get_field(instance, key):
		if key == "length":
			return len(instance)
		elif key == "chars":
			return instance

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'length', Uint, (0, None), (False, None)
		yield 'value', Array, (0, None, (cls.get_field(instance, 'length')), Char), (False, None)
