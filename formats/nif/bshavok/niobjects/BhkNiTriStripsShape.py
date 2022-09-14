# START_GLOBALS
import generated.formats.nif as NifFormat
from generated.utils.inertia import get_mass_center_inertia_polyhedron
from generated.utils.mathutils import vecAdd, vecscalarMul, matAdd
# END_GLOBALS

class BhkNiTriStripsShape:
# START_CLASS

	def get_interchangeable_packed_shape(self):
		"""Returns a bhkPackedNiTriStripsShape block that is geometrically
		interchangeable.
		"""
		# get all vertices, triangles, and calculate normals
		vertices = []
		normals = []
		triangles = []
		for strip in self.strips_data:
			triangles.extend(
				(tri1 + len(vertices),
				 tri2 + len(vertices),
				 tri3 + len(vertices))
				for tri1, tri2, tri3 in strip.get_triangles())
			vertices.extend(
				# scaling factor 1/7 applied in add_shape later
				vert.as_tuple() for vert in strip.vertices)
			normals.extend(
				(strip.vertices[tri2] - strip.vertices[tri1]).crossproduct(
					strip.vertices[tri3] - strip.vertices[tri1])
				.normalized(ignore_error=True)
				.as_tuple()
				for tri1, tri2, tri3 in strip.get_triangles())
		# create packed shape and add geometry
		packed = NifFormat.classes.BhkPackedNiTriStripsShape(self.context)
		packed.add_shape(
			triangles=triangles,
			normals=normals,
			vertices=vertices,
			# default layer 1 (static collision)
			layer=self.data_layers[0].layer if self.data_layers else 1,
			material=self.material.material)
		# set scale
		packed.scale_copy.x = 1.0
		packed.scale_copy.y = 1.0
		packed.scale_copy.z = 1.0
		packed.scale.x = 1.0
		packed.scale.y = 1.0
		packed.scale.z = 1.0
		# return result
		return packed

	def get_mass_center_inertia(self, density = 1, solid = True):
		"""Return mass, center, and inertia tensor."""
		# first find mass, center, and inertia of all shapes
		subshapes_mci = []
		for data in self.strips_data:
			subshapes_mci.append(
				get_mass_center_inertia_polyhedron(
					[ vert.as_tuple() for vert in data.vertices ],
					[ triangle for triangle in data.get_triangles() ],
					density = density, solid = solid))

		# now calculate mass, center, and inertia
		total_mass = 0
		total_center = (0, 0, 0)
		total_inertia = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
		for mass, center, inertia in subshapes_mci:
			total_mass += mass
			total_center = vecAdd(total_center,
								  vecscalarMul(center, mass / total_mass))
			total_inertia = matAdd(total_inertia, inertia)
		return total_mass, total_center, total_inertia
