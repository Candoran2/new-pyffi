# START_GLOBALS
from generated.utils.inertia import getMassInertiaSphere
# END_GLOBALS


class BhkSphereShape:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor <scale> on data."""
		# apply scale on dimensions
		self.radius *= scale

	def get_mass_center_inertia(self, density = 1, solid = True):
		"""Return mass, center, and inertia tensor."""
		# the dimensions describe half the size of the box in each dimension
		# so the length of a single edge is dimension.dir * 2
		mass, inertia = getMassInertiaSphere(
			self.radius, density = density, solid = solid)
		return mass, (0,0,0), inertia
