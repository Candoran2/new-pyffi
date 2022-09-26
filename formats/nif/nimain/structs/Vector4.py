# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS


class Vector4:
# START_CLASS

	def __init__(self, context=None, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.x = 0
		self.y = 0
		self.z = 0
		self.w = 0

	@classmethod
	def from_value(cls, in_it):
		instance = cls()
		instance.x = in_it[0]
		instance.y = in_it[1]
		instance.z = in_it[2]
		instance.w = in_it[3]
		return instance

	def as_list(self):
		return [self.x, self.y, self.z, self.w]

	def as_tuple(self):
		return (self.x, self.y, self.z, self.w)

	def get_copy(self):
		v = Vector4()
		v.x = self.x
		v.y = self.y
		v.z = self.z
		v.w = self.w
		return v

	def get_vector_3(self):
		v = NifFormat.classes.Vector3()
		v.x = self.x
		v.y = self.y
		v.z = self.z
		return v

	def __str__(self):
		return "[ %6.3f %6.3f %6.3f %6.3f ]"%(self.x, self.y, self.z, self.w)

	def __eq__(self, rhs):
		if isinstance(rhs, type(None)):
			return False
		if not isinstance(rhs, Vector4):
			raise TypeError(
				"do not know how to compare Vector4 and %s" % rhs.__class__)
		if abs(self.x - rhs.x) > NifFormat.EPSILON: return False
		if abs(self.y - rhs.y) > NifFormat.EPSILON: return False
		if abs(self.z - rhs.z) > NifFormat.EPSILON: return False
		if abs(self.w - rhs.w) > NifFormat.EPSILON: return False
		return True

	def __ne__(self, rhs):
		return not self.__eq__(rhs)

	@staticmethod
	def validate_instance(instance, context=None, arguments=()):
		Float.validate_instance(instance.x)
		Float.validate_instance(instance.y)
		Float.validate_instance(instance.z)
		Float.validate_instance(instance.w)
