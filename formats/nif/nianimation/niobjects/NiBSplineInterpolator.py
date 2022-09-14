class NiBSplineInterpolator:
# START_CLASS
	def get_times(self):
		"""Return an iterator over all key times.

		@todo: When code for calculating the bsplines is ready, this function
		will return exactly self.basis_data.num_control_points - 1 time points, and
		not self.basis_data.num_control_points as it is now.
		"""
		# is there basis data?
		if not self.basis_data:
			return
		# return all times
		for i in range(self.basis_data.num_control_points):
			yield (
				self.start_time
				+ (i * (self.stop_time - self.start_time)
				   / (self.basis_data.num_control_points - 1))
				)

	def _getFloatKeys(self, offset, element_size):
		"""Helper function to get iterator to various keys. Internal use only."""
		# are there keys?
		if offset == 65535:
			return
		# is there basis data and spline data?
		if not self.basis_data or not self.spline_data:
			return
		# yield all keys
		for key in self.spline_data.get_float_data(offset,
												self.basis_data.num_control_points,
												element_size):
			yield key

	def _getCompKeys(self, offset, element_size, bias, multiplier):
		"""Helper function to get iterator to various keys. Internal use only."""
		# are there keys?
		if offset == 65535:
			return
		# is there basis data and spline data?
		if not self.basis_data or not self.spline_data:
			return
		# yield all keys
		for key in self.spline_data.get_comp_data(offset,
											   self.basis_data.num_control_points,
											   element_size,
											   bias, multiplier):
			yield key
