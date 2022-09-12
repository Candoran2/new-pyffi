class BhkRagdollConstraint:
	def apply_scale(self, scale):
		"""Scale data."""
		# apply scale on transform
		self.ragdoll.pivot_a.x *= scale
		self.ragdoll.pivot_a.y *= scale
		self.ragdoll.pivot_a.z *= scale
		self.ragdoll.pivot_b.x *= scale
		self.ragdoll.pivot_b.y *= scale
		self.ragdoll.pivot_b.z *= scale

	def update_a_b(self, parent):
		"""Update the B data from the A data."""
		self.ragdoll.update_a_b(self.get_transform_a_b(parent))
