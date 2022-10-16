class Color4:
# START_CLASS

	def __init__(self, context=None, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.r = 0
		self.g = 0
		self.b = 0
		self.a = 0

	@classmethod
	def from_value(cls, in_it):
		instance = cls()
		instance.r = in_it[0]
		instance.g = in_it[1]
		instance.b = in_it[2]
		instance.a = in_it[3]
		return instance

	@staticmethod
	def validate_instance(instance, context=None, arg=0, template=None):
		Float.validate_instance(instance.r)
		Float.validate_instance(instance.g)
		Float.validate_instance(instance.b)
		Float.validate_instance(instance.a)
