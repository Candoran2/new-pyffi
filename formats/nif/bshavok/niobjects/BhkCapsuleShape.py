# START_GLOBALS
from generated.utils.inertia import getMassInertiaCapsule
import generated.utils.mathutils as m_util
# END_GLOBALS


class BhkCapsuleShape:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor <scale> on data."""
		# apply scale on dimensions
		self.radius *= scale
		self.radius_1 *= scale
		self.radius_2 *= scale
		self.first_point.x *= scale
		self.first_point.y *= scale
		self.first_point.z *= scale
		self.second_point.x *= scale
		self.second_point.y *= scale
		self.second_point.z *= scale

	def get_mass_center_inertia(self, density = 1, solid = True):
		"""Return mass, center, and inertia tensor."""
		# (assumes self.radius == self.radius_1 == self.radius_2)
		length = (self.first_point - self.second_point).norm()
		mass, inertia = getMassInertiaCapsule(
			radius = self.radius, length = length,
			density = density, solid = solid)
		# now fix inertia so it is expressed in the right coordinates
		# need a transform that maps (0,0,length/2) on (second - first) / 2
		# and (0,0,-length/2) on (first - second)/2
		vec1 = ((self.second_point - self.first_point) / length).as_tuple()
		# find an orthogonal vector to vec1
		index = min(enumerate(vec1), key=lambda val: abs(val[1]))[0]
		vec2 = m_util.vecCrossProduct(vec1, tuple((1 if i == index else 0)
										   for i in range(3)))
		vec2 = m_util.vecscalarMul(vec2, 1/m_util.vecNorm(vec2))
		# find an orthogonal vector to vec1 and vec2
		vec3 = m_util.vecCrossProduct(vec1, vec2)
		# get transform matrix
		transform_transposed = (vec2, vec3, vec1) # this is effectively the transposed of our transform
		transform = m_util.matTransposed(transform_transposed)
		# check the result (debug)
		assert(m_util.vecDistance(m_util.matvecMul(transform, (0,0,1)), vec1) < 0.0001)
		assert(abs(m_util.matDeterminant(transform) - 1) < 0.0001)
		# transform the inertia tensor
		inertia = m_util.matMul(m_util.matMul(transform_transposed, inertia), transform)
		return (mass,
				((self.first_point + self.second_point) * 0.5).as_tuple(),
				inertia)