class NiTransformInterpolator:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor <scale> on data."""
		super().apply_scale(scale)
		# apply scale on translation
		self.transform.apply_scale(scale)
