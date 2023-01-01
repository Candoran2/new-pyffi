class NiBSplineCompTransformInterpolator:
# START_CLASS

	def get_translations(self):
		"""Return an iterator over all translation keys."""
		return self._getCompKeys(self.translation_handle, 3,
								 self.translation_offset, self.translation_half_range)

	def get_rotations(self):
		"""Return an iterator over all rotation keys."""
		return self._getCompKeys(self.rotation_handle, 4,
								 self.rotation_offset, self.rotation_half_range)

	def get_scales(self):
		"""Return an iterator over all scale keys."""
		for key in self._getCompKeys(self.scale_handle, 1,
									 self.scale_offset, self.scale_half_range):
			yield key[0]

	def apply_scale(self, scale):
		"""Apply scale factor on data."""
		super().apply_scale(scale)
		self.translation_offset *= scale
		self.translation_half_range *= scale
