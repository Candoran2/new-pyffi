class Vector3:
# START_CLASS

	def __init__(self, context=None, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.x = 0
		self.y = 0
		self.z = 0

	@classmethod
	def from_value(cls, in_it):
		instance = cls()
		instance.x = in_it[0]
		instance.y = in_it[1]
		instance.z = in_it[2]
		return instance