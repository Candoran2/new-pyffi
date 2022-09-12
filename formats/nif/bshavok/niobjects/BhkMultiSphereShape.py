# START_GLOBALS
from generated.utils.inertia import getMassInertiaSphere
from generated.utils.mathutils import vecAdd, vecscalarMul, matAdd
# END_GLOBALS

class BhkMultiSphereShape:
	def get_mass_center_inertia(self, density = 1, solid = True):
		"""Return center of gravity and area."""
		subshapes_mci = [
			(mass, center, inertia)
			for (mass, inertia), center in
			zip( ( getMassInertiaSphere(radius = sphere.radius,
															 density = density, solid = solid)
					for sphere in self.spheres ),
				  ( sphere.center.as_tuple() for sphere in self.spheres ) ) ]
		total_mass = 0
		total_center = (0, 0, 0)
		total_inertia = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
		for mass, center, inertia in subshapes_mci:
			total_mass += mass
			total_center = vecAdd(total_center,
								  vecscalarMul(center, mass / total_mass))
			total_inertia = matAdd(total_inertia, inertia)
		return total_mass, total_center, total_inertia
