class BhkRagdollConstraintCInfo:
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
		plane_b = self.plane_a.get_vector_3() *  transform
		twist_b = self.twist_a.get_vector_3() *  transform
		self.plane_b.x = plane_b.x
		self.plane_b.y = plane_b.y
		self.plane_b.z = plane_b.z
		self.twist_b.x = twist_b.x
		self.twist_b.y = twist_b.y
		self.twist_b.z = twist_b.z
