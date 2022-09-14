# START_GLOBALS
import generated.formats.nif as NifFormat
from generated.utils.inertia import get_mass_center_inertia_polyhedron
from generated.utils.quickhull import qhull3d
# END_GLOBALS


class BhkConvexVerticesShape:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor on data."""
		if abs(scale - 1.0) < NifFormat.EPSILON: return
		for v in self.vertices:
			v.x *= scale
			v.y *= scale
			v.z *= scale
		for n in self.normals:
			n.w *= scale

	def get_mass_center_inertia(self, density = 1, solid = True):
		"""Return mass, center, and inertia tensor."""
		# first find an enumeration of all triangles making up the convex shape
		vertices, triangles = qhull3d(
			[vert.as_tuple() for vert in self.vertices])
		# now calculate mass, center, and inertia
		return get_mass_center_inertia_polyhedron(
			vertices, triangles, density = density, solid = solid)
