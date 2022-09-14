class NiBSplineTransformInterpolator:
# START_CLASS
	def get_translations(self):
		"""Return an iterator over all translation keys."""
		return self._getFloatKeys(self.translation_offset, 3)

	def get_rotations(self):
		"""Return an iterator over all rotation keys."""
		return self._getFloatKeys(self.rotation_offset, 4)

	def get_scales(self):
		"""Return an iterator over all scale keys."""
		for key in self._getFloatKeys(self.scale_offset, 1):
			yield key[0]

	def apply_scale(self, scale):
		"""Apply scale factor on data."""
		self.translation.x *= scale
		self.translation.y *= scale
		self.translation.z *= scale
		# also scale translation float keys
		if self.translation_offset != 65535:
			offset = self.translation_offset
			num_elements = self.basis_data.num_control_points
			element_size = 3
			controlpoints = self.spline_data.float_control_points
			for element in range(num_elements):
				for index in range(element_size):
					controlpoints[offset + element * element_size + index] *= scale
