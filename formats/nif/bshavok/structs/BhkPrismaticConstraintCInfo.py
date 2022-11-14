class BhkPrismaticConstraintCInfo:
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
		self.min_distance *= scale
		self.max_distance *= scale

	def update_a_b(self, transform):
		"""Update B pivot and axes from A using the given transform."""
		# pivot point
		pivot_b = ((self.context.havok_scale * self.pivot_a.get_vector_3()) * transform) / self.context.havok_scale
		self.pivot_b.x = pivot_b.x
		self.pivot_b.y = pivot_b.y
		self.pivot_b.z = pivot_b.z
		# axes (rotation only)
		transform = transform.get_matrix_33()
		sliding_b = self.sliding_a.get_vector_3() *  transform
		rotation_b = self.rotation_a.get_vector_3() *  transform
		plane_b = self.plane_a.get_vector_3() *  transform
		self.sliding_b.x = sliding_b.x
		self.sliding_b.y = sliding_b.y
		self.sliding_b.z = sliding_b.z
		self.rotation_b.x = rotation_b.x
		self.rotation_b.y = rotation_b.y
		self.rotation_b.z = rotation_b.z
		self.plane_b.x = plane_b.x
		self.plane_b.y = plane_b.y
		self.plane_b.z = plane_b.z
