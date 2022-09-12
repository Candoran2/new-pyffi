class BSStreamHeader(BaseStruct):
# START_CLASS

	@classmethod
	def from_bs_version(cls, context, bs_version):
		instance = cls(context)
		instance.bs_version = bs_version
		for f_name, f_type, arguments, (optional, default) in cls._get_filtered_attribute_list(instance):
			if f_name == "bs_version":
				continue
			else:
				if default is None:
					field_value = f_type(instance, *arguments)
				else:
					field_value = f_type.from_value(*arguments[2:4], default)
			setattr(instance, f_name, field_value)
		return instance
