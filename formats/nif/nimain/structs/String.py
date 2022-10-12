from generated.formats.nif.structs.SizedString import SizedString
from generated.formats.nif.basic import NiFixedString

class String:

# START_CLASS

	def __new__(self, context, arg=0, template=None, set_default=True):
		return ''

	@staticmethod
	def from_stream(stream, context, arg=0, template=None):
		if context.version <= 335544325:
			return SizedString.from_stream(stream, context, 0, None)
		if context.version >= 335609859:
			return NiFixedString.from_stream(stream, context, 0, None)

	@staticmethod
	def to_stream(instance, stream, context, arg=0, template=None):
		if stream.context.version <= 335544325:
			SizedString.to_stream(instance, stream, context)
		if stream.context.version >= 335609859:
			NiFixedString.to_stream(instance, stream, context)

	@staticmethod
	def get_size(context, instance, arguments=()):
		if context.version <= 335544325:
			return SizedString.get_size(context, instance)
		if context.version >= 335609859:
			return NiFixedString.get_size(context, instance)

	get_field = None
	_get_filtered_attribute_list = None

	@staticmethod
	def fmt_member(instance, indent=0):
		return repr(instance)

	@classmethod
	def validate_instance(cls, instance, context=None, arguments=()):
		# either it contained a sizedstring or it referred to one in the header
		return SizedString.validate_instance(instance, context, (0, None))

	@staticmethod
	def from_value(value):
		return str(value)
