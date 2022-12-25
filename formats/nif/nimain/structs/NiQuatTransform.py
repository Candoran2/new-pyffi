class NiQuatTransform:

# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor <scale> on data."""
		self.translation.x *= scale
		self.translation.y *= scale
		self.translation.z *= scale