class NiTransformInterpolator:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor <scale> on data."""
		# apply scale on translation
		self.transform.apply_scale(scale)
