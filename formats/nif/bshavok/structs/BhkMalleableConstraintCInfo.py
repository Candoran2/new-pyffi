class BbhkMalleableConstraintCInfo:
# START_CLASS

	constraint_fields = ['ball_and_socket',
					     'hinge',
						 'limited_hinge',
						 'prismatic',
						 'ragdoll',
						 'stiff_spring',
						 ]

	def apply_scale(self, scale):
		for field_name in self.constraint_fields:
			getattr(self, field_name).apply_scale(scale)

	def update_a_b(self, transform):
		"""Update B pivot and axes from A using the given transform."""
		for field_name in self.constraint_fields:
			getattr(self, field_name).update_a_b(transform)
