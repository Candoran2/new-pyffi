# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS

class BSTriShape:
# START_CLASS

	def update_center_radius(self):
		"""Recalculate center and radius of the data."""
		# in case there are no vertices, set center and radius to zero
		if len(self.vertex_data) == 0:
			self.bounding_sphere.center.x = 0.0
			self.bounding_sphere.center.y = 0.0
			self.bounding_sphere.center.z = 0.0
			self.bounding_sphere.radius = 0.0
			return

		vertices = [data.vertex for data in self.vertex_data]
		# find extreme values in x, y, and z direction
		lowx = min([v.x for v in vertices])
		lowy = min([v.y for v in vertices])
		lowz = min([v.z for v in vertices])
		highx = max([v.x for v in vertices])
		highy = max([v.y for v in vertices])
		highz = max([v.z for v in vertices])

		# center is in the center of the bounding box
		cx = (lowx + highx) * 0.5
		cy = (lowy + highy) * 0.5
		cz = (lowz + highz) * 0.5
		self.bounding_sphere.center.x = cx
		self.bounding_sphere.center.y = cy
		self.bounding_sphere.center.z = cz

		# radius is the largest distance from the center
		r2 = 0.0
		for v in vertices:
			dx = cx - v.x
			dy = cy - v.y
			dz = cz - v.z
			r2 = max(r2, dx*dx+dy*dy+dz*dz)
		self.bounding_sphere.radius = r2 ** 0.5

	def apply_scale(self, scale):
		if abs(scale - 1.0) <= NifFormat.EPSILON: return
		super().apply_scale(scale)
		self.bounding_sphere.apply_scale(scale)
		for v_data in self.vertex_data:
			v = v_data.vertex
			v.x *= scale
			v.y *= scale
			v.z *= scale

	def get_triangles(self):
		"""Return triangles"""
		if self.vertex_desc.vertex_attributes.skinned:
			# triangles are found in the partition
			triangles = []
			if self.skin:
				for partition in self.skin.skin_partition.partitions:
                    # there is a vertex map, but it doesn't seem to be used
					if partition.has_faces:
						triangles.extend(partition.triangles)
			return triangles
		else:
			return self.triangles

	def get_vertex_data(self):
		vertex_data = self.vertex_data
		if self.vertex_desc.vertex_attributes.skinned:
			if self.skin:
				if self.skin.skin_partition:
					vertex_data = self.skin.skin_partition.vertex_data
		return vertex_data

	def is_skin(self):
		"""Returns True if geometry is skinned."""
		return self.skin != None

	@property
	def skin_instance(self):
		return self.skin

	@skin_instance.setter
	def skin_instance(self, value):
		self.skin = value
