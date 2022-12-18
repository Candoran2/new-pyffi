# START_GLOBALS
from generated.utils.mathutils import matTransposed, matvecMul, vecAdd, matMul
# END_GLOBALS


class BhkConvexTransformShape:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor <scale> on data."""
		# apply scale on translation
		self.transform.m_14 *= scale
		self.transform.m_24 *= scale
		self.transform.m_34 *= scale

	def get_mass_center_inertia(self, density=1, solid=True):
		"""Return mass, center, and inertia tensor."""
		# get shape mass, center, and inertia
		mass, center, inertia = self.get_shape_mass_center_inertia(
			density=density, solid=solid)
		# get transform matrix and translation vector
		transform = self.transform.get_matrix_33().as_tuple()
		transform_transposed = matTransposed(transform)
		translation = ( self.transform.m_14, self.transform.m_24, self.transform.m_34 )
		# transform center and inertia
		center = matvecMul(transform, center)
		center = vecAdd(center, translation)
		inertia = matMul(matMul(transform_transposed, inertia), transform)
		# return updated mass center and inertia
		return mass, center, inertia

