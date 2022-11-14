class BhkHingeConstraintCInfo:
# START_CLASS

	def apply_scale(self, scale):
		"""Scale data."""
		# apply scale on transform
		self.pivot_a.x *= scale
		self.pivot_a.y *= scale
		self.pivot_a.z *= scale
		self.pivot_b.x *= scale
		self.pivot_b.y *= scale
		self.pivot_b.z *= scale

	def update_a_b(self, transform):
		"""Update B pivot and axes from A using the given transform."""
		# pivot point
		pivot_b = ((self.context.havok_scale * self.pivot_a.get_vector_3()) * transform) / self.context.havok_scale
		self.pivot_b.x = pivot_b.x
		self.pivot_b.y = pivot_b.y
		self.pivot_b.z = pivot_b.z
		# axes (rotation only)
		transform = transform.get_matrix_33()
		axis_b = self.axis_a.get_vector_3() *  transform
		perp_axis_in_b_1 = self.perp_axis_in_a_1.get_vector_3() * transform
		perp_axis_in_b_2 = self.perp_axis_in_a_2.get_vector_3() * transform
		self.axis_b.x = axis_b.x
		self.axis_b.y = axis_b.y
		self.axis_b.z = axis_b.z
		self.perp_axis_in_b_1.x = perp_axis_in_b_1.x
		self.perp_axis_in_b_1.y = perp_axis_in_b_1.y
		self.perp_axis_in_b_1.z = perp_axis_in_b_1.z
		self.perp_axis_in_b_2.x = perp_axis_in_b_2.x
		self.perp_axis_in_b_2.y = perp_axis_in_b_2.y
		self.perp_axis_in_b_2.z = perp_axis_in_b_2.z
