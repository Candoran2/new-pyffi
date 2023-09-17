class BSBound:
# START_CLASS

	def apply_scale(self, scale):
		"""Scale data."""
		super().apply_scale(scale)
		self.center.x *= scale
		self.center.y *= scale
		self.center.z *= scale
		self.dimensions.x *= scale
		self.dimensions.y *= scale
		self.dimensions.z *= scale
