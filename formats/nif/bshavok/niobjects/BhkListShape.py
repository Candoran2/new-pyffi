# START_GLOBALS
from generated.utils.mathutils import vecAdd, vecscalarMul, matAdd
# END_GLOBALS

class BhkListShape:
	def get_mass_center_inertia(self, density = 1, solid = True):
		"""Return center of gravity and area."""
		subshapes_mci = [ subshape.get_mass_center_inertia(density = density,
														solid = solid)
						  for subshape in self.sub_shapes ]
		total_mass = 0
		total_center = (0, 0, 0)
		total_inertia = ((0, 0, 0), (0, 0, 0), (0, 0, 0))

		# get total mass
		for mass, center, inertia in subshapes_mci:
			total_mass += mass
		if total_mass == 0:
			return 0, (0, 0, 0), ((0, 0, 0), (0, 0, 0), (0, 0, 0))

		# get average center and inertia
		for mass, center, inertia in subshapes_mci:
			total_center = vecAdd(total_center,
								  vecscalarMul(center, mass / total_mass))
			total_inertia = matAdd(total_inertia, inertia)
		return total_mass, total_center, total_inertia

	def add_shape(self, shape, front = False):
		"""Add shape to list."""
		# check if it's already there
		if shape in self.sub_shapes: return
		# increase number of shapes
		num_shapes = self.num_sub_shapes
		self.num_sub_shapes = num_shapes + 1
		# add the shape
		if not front:
			self.sub_shapes.append(shape)
		else:
			self.sub_shapes[:] = [shape, *self.sub_shapes]
		# expand list of unknown ints as well
		self.num_unknown_ints = num_shapes + 1
		self.unknown_ints.append(0)

	def remove_shape(self, shape):
		"""Remove a shape from the shape list."""
		# get list of shapes excluding the shape to remove
		shapes = [s for s in self.sub_shapes if s != shape]
		# set sub_shapes to this list
		self.num_sub_shapes = len(shapes)
		self.sub_shapes[:] = shapes
		# update unknown ints
		self.num_unknown_ints = len(shapes)
		self.unknown_ints[:] = (0, ) * len(shapes)
