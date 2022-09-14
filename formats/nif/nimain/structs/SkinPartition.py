# START_GLOBALS
from generated.utils.tristrip import triangulate
# END_GLOBALS

class SkinPartition:
# START_CLASS
	
	def get_triangles(self):
		"""Get list of triangles of this partition.
		"""
		# strips?
		if self.num_strips:
			for tri in triangulate(self.strips):
				yield tri
		# no strips, do triangles
		else:
			for tri in self.triangles:
				yield (tri.v_1, tri.v_2, tri.v_3)

	def get_mapped_triangles(self):
		"""Get list of triangles of this partition (mapping into the
		geometry data vertex list).
		"""
		for tri in self.get_triangles():
			yield tuple(self.vertex_map[v_index] for v_index in tri)
