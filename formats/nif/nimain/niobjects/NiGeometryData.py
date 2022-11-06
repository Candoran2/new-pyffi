# START_GLOBALS
from generated.utils.mathutils import float_to_int
import generated.formats.nif as NifFormat
# END_GLOBALS

class NiGeometryData:
# START_CLASS
	"""
	>>> from pyffi.formats.nif import NifFormat
	>>> geomdata = NifFormat.NiGeometryData()
	>>> geomdata.num_vertices = 3
	>>> geomdata.has_vertices = True
	>>> geomdata.has_normals = True
	>>> geomdata.has_vertex_colors = True
	>>> geomdata.num_uv_sets = 2
	>>> geomdata.vertices.update_size()
	>>> geomdata.normals.update_size()
	>>> geomdata.vertex_colors.update_size()
	>>> geomdata.uv_sets.update_size()
	>>> geomdata.vertices[0].x = 1
	>>> geomdata.vertices[0].y = 2
	>>> geomdata.vertices[0].z = 3
	>>> geomdata.vertices[1].x = 4
	>>> geomdata.vertices[1].y = 5
	>>> geomdata.vertices[1].z = 6
	>>> geomdata.vertices[2].x = 1.200001
	>>> geomdata.vertices[2].y = 3.400001
	>>> geomdata.vertices[2].z = 5.600001
	>>> geomdata.normals[0].x = 0
	>>> geomdata.normals[0].y = 0
	>>> geomdata.normals[0].z = 1
	>>> geomdata.normals[1].x = 0
	>>> geomdata.normals[1].y = 1
	>>> geomdata.normals[1].z = 0
	>>> geomdata.normals[2].x = 1
	>>> geomdata.normals[2].y = 0
	>>> geomdata.normals[2].z = 0
	>>> geomdata.vertex_colors[1].r = 0.310001
	>>> geomdata.vertex_colors[1].g = 0.320001
	>>> geomdata.vertex_colors[1].b = 0.330001
	>>> geomdata.vertex_colors[1].a = 0.340001
	>>> geomdata.uv_sets[0][0].u = 0.990001
	>>> geomdata.uv_sets[0][0].v = 0.980001
	>>> geomdata.uv_sets[0][2].u = 0.970001
	>>> geomdata.uv_sets[0][2].v = 0.960001
	>>> geomdata.uv_sets[1][0].v = 0.910001
	>>> geomdata.uv_sets[1][0].v = 0.920001
	>>> geomdata.uv_sets[1][2].v = 0.930001
	>>> geomdata.uv_sets[1][2].v = 0.940001
	>>> for h in geomdata.get_vertex_hash_generator():
	...	 print(h)
	(1000, 2000, 3000, 0, 0, 1000, 99000, 98000, 0, 92000, 0, 0, 0, 0)
	(4000, 5000, 6000, 0, 1000, 0, 0, 0, 0, 0, 310, 320, 330, 340)
	(1200, 3400, 5600, 1000, 0, 0, 97000, 96000, 0, 94000, 0, 0, 0, 0)
	"""
	def update_center_radius(self):
		"""Recalculate center and radius of the data."""
		# in case there are no vertices, set center and radius to zero
		if len(self.vertices) == 0:
			self.bounding_sphere.center.x = 0.0
			self.bounding_sphere.center.y = 0.0
			self.bounding_sphere.center.z = 0.0
			self.bounding_sphere.radius = 0.0
			return

		# find extreme values in x, y, and z direction
		lowx = min([v.x for v in self.vertices])
		lowy = min([v.y for v in self.vertices])
		lowz = min([v.z for v in self.vertices])
		highx = max([v.x for v in self.vertices])
		highy = max([v.y for v in self.vertices])
		highz = max([v.z for v in self.vertices])

		# center is in the center of the bounding box
		cx = (lowx + highx) * 0.5
		cy = (lowy + highy) * 0.5
		cz = (lowz + highz) * 0.5
		self.bounding_sphere.center.x = cx
		self.bounding_sphere.center.y = cy
		self.bounding_sphere.center.z = cz

		# radius is the largest distance from the center
		r2 = 0.0
		for v in self.vertices:
			dx = cx - v.x
			dy = cy - v.y
			dz = cz - v.z
			r2 = max(r2, dx*dx+dy*dy+dz*dz)
		self.bounding_sphere.radius = r2 ** 0.5

	def apply_scale(self, scale):
		"""Apply scale factor on data."""
		if abs(scale - 1.0) <= NifFormat.EPSILON: return
		for v in self.vertices:
			v.x *= scale
			v.y *= scale
			v.z *= scale
		self.bounding_sphere.apply_scale(scale)

	def get_vertex_hash_generator(
		self,
		vertexprecision=3, normalprecision=3,
		uvprecision=5, vcolprecision=3):
		"""Generator which produces a tuple of integers for each
		(vertex, normal, uv, vcol), to ease detection of duplicate
		vertices. The precision parameters denote number of
		significant digits behind the comma.

		Default for uvprecision should really be high because for
		very large models the uv coordinates can be very close
		together.

		For vertexprecision, 3 seems usually enough (maybe we'll
		have to increase this at some point).

		:param vertexprecision: Precision to be used for vertices.
		:type vertexprecision: float
		:param normalprecision: Precision to be used for normals.
		:type normalprecision: float
		:param uvprecision: Precision to be used for uvs.
		:type uvprecision: float
		:param vcolprecision: Precision to be used for vertex colors.
		:type vcolprecision: float
		:return: A generator yielding a hash value for each vertex.
		"""
		
		verts = self.vertices if self.has_vertices else None
		norms = self.normals if self.has_normals else None
		uvsets = self.uv_sets if len(self.uv_sets) else None
		vcols = self.vertex_colors if self.has_vertex_colors else None
		vertexfactor = 10 ** vertexprecision
		normalfactor = 10 ** normalprecision
		uvfactor = 10 ** uvprecision
		vcolfactor = 10 ** vcolprecision
		for i in range(self.num_vertices):
			h = []
			if verts:
				h.extend([float_to_int(x * vertexfactor)
						 for x in [verts[i].x, verts[i].y, verts[i].z]])
			if norms:
				h.extend([float_to_int(x * normalfactor)
						  for x in [norms[i].x, norms[i].y, norms[i].z]])
			if uvsets:
				for uvset in uvsets:
					# uvs sometimes have NaN, for example:
					# oblivion/meshes/architecture/anvil/anvildooruc01.nif
					h.extend([float_to_int(x * uvfactor)
							  for x in [uvset[i].u, uvset[i].v]])
			if vcols:
				h.extend([float_to_int(x * vcolfactor)
						  for x in [vcols[i].r, vcols[i].g,
									vcols[i].b, vcols[i].a]])
			yield tuple(h)
