class BhkRefObject:
	def get_shape_mass_center_inertia(self, density=1, solid=True):
		"""Return mass, center of gravity, and inertia tensor of
		this object's shape, if self.shape is not None.

		If self.shape is None, then returns zeros for everything.
		"""
		if not self.shape:
			mass = 0
			center = (0, 0, 0)
			inertia = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
		else:
			mass, center, inertia = self.shape.get_mass_center_inertia(
				density=density, solid=solid)
		return mass, center, inertia
