from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.nif.basic import Byte
from generated.formats.nif.basic import Char


class ExportString(BaseStruct):


# START_CLASS

	def __new__(self, context, arg=0, template=None, set_default=True):
		return ''

	@staticmethod
	def from_stream(stream, context=None, arg=0, template=None):
		length = Byte.from_stream(stream)
		chars = stream.read(length)[:-1]
		return chars.decode(errors="surrogateescape")

	@staticmethod
	def to_stream(stream, instance):
		instance = instance + '\x00'
		length = len(instance)
		Byte.to_stream(stream, length)
		stream.write(instance.encode(errors="surrogateescape"))

	@staticmethod
	def get_field(instance, key):
		if key == "length":
			return len(instance)
		elif key == "chars":
			return instance
