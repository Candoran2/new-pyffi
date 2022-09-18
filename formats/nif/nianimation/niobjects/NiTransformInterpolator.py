class NiTransformInterpolator:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor <scale> on data."""
		# apply scale on translation
		self.transform.translation.x *= scale
		self.transform.translation.y *= scale
		self.transform.translation.z *= scale
