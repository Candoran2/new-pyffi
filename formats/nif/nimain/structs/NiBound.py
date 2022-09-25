class NiBound:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor on data.

		:param scale: The scale factor."""
		self.center *= scale
		self.radius *= scale
		if hasattr(self, "div2_aabb"):
			for vector in self.div2_aabb.corners:
				vector.x *= scale
				vector.y *= scale
				vector.z *= scale
