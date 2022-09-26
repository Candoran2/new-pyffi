# START_GLOBALS
from generated.utils.vertex_cache import stripify
from generated.utils.tristrip import triangulate
# END_GLOBALS

class NiTriShapeData:
# START_CLASS
	"""
	Example usage:

	>>> from pyffi.formats.nif import NifFormat
	>>> block = NifFormat.NiTriShapeData()
	>>> block.set_triangles([(0,1,2),(2,1,3),(2,3,4)])
	>>> block.get_strips()
	[[0, 1, 2, 3, 4]]
	>>> block.get_triangles()
	[(0, 1, 2), (2, 1, 3), (2, 3, 4)]
	>>> block.set_strips([[1,0,1,2,3,4]])
	>>> block.get_strips() # stripifier keeps geometry but nothing else
	[[0, 2, 1, 3], [2, 4, 3]]
	>>> block.get_triangles()
	[(0, 2, 1), (1, 2, 3), (2, 4, 3)]
	"""
	def get_triangles(self):
		return [(t.v_1, t.v_2, t.v_3) for t in self.triangles]

	def set_triangles(self, triangles, stitchstrips = False):
		# note: the stitchstrips argument is ignored - only present to ensure
		# uniform interface between NiTriShapeData and NiTriStripsData

		# initialize triangle array
		n = len(triangles)
		self.num_triangles = n
		self.num_triangle_points = 3*n
		self.has_triangles = (n > 0)
		self.reset_field("triangles")

		# set triangles to triangles array
		for dst_t, src_t in zip(self.triangles, triangles):
			dst_t.v_1, dst_t.v_2, dst_t.v_3 = src_t

	def get_strips(self):
		return stripify(self.get_triangles())

	def set_strips(self, strips):
		self.set_triangles(triangulate(strips))
