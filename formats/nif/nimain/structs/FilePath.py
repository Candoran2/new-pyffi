from generated.formats.nif.imports import name_type_map

class FilePath:

# START_CLASS

	def __new__(self, context, arg=0, template=None, set_default=True):
		return ''

	@staticmethod
	def from_stream(stream, context, arg=0, template=None):
		if context.version <= 335544325:
			return name_type_map["SizedString"].from_stream(stream, context, 0, None)
		if context.version >= 335609859:
			return name_type_map["NiFixedString"].from_stream(stream, context, 0, None)

	@staticmethod
	def to_stream(instance, stream, context, arg=0, template=None):
		if stream.context.version <= 335544325:
			name_type_map["SizedString"].to_stream(instance, stream, context)
		if stream.context.version >= 335609859:
			name_type_map["NiFixedString"].to_stream(instance, stream, context)

	@staticmethod
	def get_size(instance, context, arg=0, template=None):
		if context.version <= 335544325:
			return name_type_map["SizedString"].get_size(instance, context)
		if context.version >= 335609859:
			return name_type_map["NiFixedString"].get_size(instance, context)

	get_field = None
	_get_filtered_attribute_list = None

	@staticmethod
	def fmt_member(instance, indent=0):
		return repr(instance)

	@classmethod
	def validate_instance(cls, instance, context=None, arg=0, template=None):
		# either it contained a sizedstring or it referred to one in the header
		return name_type_map["SizedString"].validate_instance(instance, context, 0, None)
