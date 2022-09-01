class TexCoord:
# START_CLASS

	def __init__(self, context=None, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u = 0
		self.v = 0

	@classmethod
	def from_value(cls, in_it):
		instance = cls()
		instance.u = in_it[0]
		instance.v = in_it[1]
		return instance