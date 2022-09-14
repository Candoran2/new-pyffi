class NiBSplineCompTransformInterpolator:
# START_CLASS

	def get_translations(self):
		"""Return an iterator over all translation keys."""
		return self._getCompKeys(self.translation_offset, 3,
								 self.translation_bias, self.translation_multiplier)

	def get_rotations(self):
		"""Return an iterator over all rotation keys."""
		return self._getCompKeys(self.rotation_offset, 4,
								 self.rotation_bias, self.rotation_multiplier)

	def get_scales(self):
		"""Return an iterator over all scale keys."""
		for key in self._getCompKeys(self.scale_offset, 1,
									 self.scale_bias, self.scale_multiplier):
			yield key[0]

	def apply_scale(self, scale):
		"""Apply scale factor on data."""
		self.translation.x *= scale
		self.translation.y *= scale
		self.translation.z *= scale
		self.translation_bias *= scale
		self.translation_multiplier *= scale
