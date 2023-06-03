class NiBSplineTransformInterpolator:
# START_CLASS
	def get_translations(self):
		"""Return an iterator over all translation keys."""
		return self._getFloatKeys(self.translation_handle, 3)

	def get_rotations(self):
		"""Return an iterator over all rotation keys."""
		return self._getFloatKeys(self.rotation_handle, 4)

	def get_scales(self):
		"""Return an iterator over all scale keys."""
		for key in self._getFloatKeys(self.scale_handle, 1):
			yield key[0]

	def apply_scale(self, scale):
		"""Apply scale factor on data."""
		self.transform.apply_scale(scale)
		# also scale translation float keys
		if self.translation_handle != 65535:
			offset = self.translation_handle
			num_elements = self.basis_data.num_control_points
			element_size = 3
			point_types = (self.spline_data.float_control_points, )
			for controlpoints in point_types:
				if len(controlpoints) > 0:
					for element in range(num_elements):
						for index in range(element_size):
							controlpoints[offset + element * element_size + index] *= scale
