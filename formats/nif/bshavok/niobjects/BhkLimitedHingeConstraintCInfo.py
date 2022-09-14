class BhkLimitedHingeConstraintCInfo:
# START_CLASS

	def update_a_b(self, transform):
		"""Update B pivot and axes from A using the given transform."""
		# pivot point
		pivot_b = ((7 * self.pivot_a.get_vector_3()) * transform) / 7.0
		self.pivot_b.x = pivot_b.x
		self.pivot_b.y = pivot_b.y
		self.pivot_b.z = pivot_b.z
		# axes (rotation only)
		transform = transform.get_matrix_33()
		axle_b = self.axle_a.get_vector_3() *  transform
		perp_2_axle_in_b_2 = self.perp_2_axle_in_a_2.get_vector_3() * transform
		self.axle_b.x = axle_b.x
		self.axle_b.y = axle_b.y
		self.axle_b.z = axle_b.z
		self.perp_2_axle_in_b_2.x = perp_2_axle_in_b_2.x
		self.perp_2_axle_in_b_2.y = perp_2_axle_in_b_2.y
		self.perp_2_axle_in_b_2.z = perp_2_axle_in_b_2.z
