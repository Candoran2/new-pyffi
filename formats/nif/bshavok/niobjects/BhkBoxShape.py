# START_GLOBALS
from generated.utils.inertia import getMassInertiaBox
# END_GLOBALS


class BhkBoxShape:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor C{scale} on data."""
		super().apply_scale(scale)
		# apply scale on dimensions
		self.dimensions.x *= scale
		self.dimensions.y *= scale
		self.dimensions.z *= scale
		self.unused_float  *= scale

	def get_mass_center_inertia(self, density = 1, solid = True):
		"""Return mass, center, and inertia tensor."""
		# the dimensions describe half the size of the box in each dimension
		# so the length of a single edge is dimension.dir * 2
		mass, inertia = getMassInertiaBox(
			(self.dimensions.x * 2, self.dimensions.y * 2, self.dimensions.z * 2),
			density = density, solid = solid)
		return mass, (0,0,0), inertia