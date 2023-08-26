# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS


class BSSkinBoneTrans:
# START_CLASS
	def get_transform(self):
		"""Return scale, rotation, and translation into a single 4x4 matrix."""
		mat = NifFormat.classes.Matrix44()
		mat.set_scale_rotation_translation(
			self.scale,
			self.rotation,
			self.translation)
		return mat

	def set_transform(self, mat):
		"""Set rotation, transform, and velocity."""
		scale, rotation, translation = mat.get_scale_rotation_translation()

		self.scale = scale

		self.rotation.m_11 = rotation.m_11
		self.rotation.m_12 = rotation.m_12
		self.rotation.m_13 = rotation.m_13
		self.rotation.m_21 = rotation.m_21
		self.rotation.m_22 = rotation.m_22
		self.rotation.m_23 = rotation.m_23
		self.rotation.m_31 = rotation.m_31
		self.rotation.m_32 = rotation.m_32
		self.rotation.m_33 = rotation.m_33

		self.translation.x = translation.x
		self.translation.y = translation.y
		self.translation.z = translation.z
