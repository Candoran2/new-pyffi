class BoneData:
# START_CLASS
	def get_transform(self):
		"""Return scale, rotation, and translation into a single 4x4 matrix."""
		return self.skin_transform.get_transform()

	def set_transform(self, mat):
		"""Set rotation, transform, and velocity."""
		self.skin_transform.set_transform(mat)
