class BoundingVolume:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor on data.

		:param scale: The scale factor."""
		if hasattr(self, "sphere"):
			self.sphere.apply_scale(scale)
		if hasattr(self, "box"):
			self.box.center *= scale
			self.box.extent *= scale
		if hasattr(self, "capsule"):
			self.capsule.center *= scale
			self.capsule.origin *= scale
			self.capsule.extent *= scale
			self.capsule.radius *= scale
		if hasattr(self, "half_space"):
			self.half_space.plane.constant *= scale
			self.half_space.center *= scale
