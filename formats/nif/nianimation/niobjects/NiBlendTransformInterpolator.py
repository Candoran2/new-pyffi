class NiBlendTransformInterpolator:

# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor <scale> on data."""
		super().apply_scale(scale)
		self.value.apply_scale(scale)