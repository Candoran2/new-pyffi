# START_GLOBALS
from generated.utils.vertex_cache import stripify
from generated.utils.tristrip import triangulate
# END_GLOBALS

class NiTriStripsData:
# START_CLASS
	"""
	Example usage:

	>>> from pyffi.formats.nif import NifFormat
	>>> block = NifFormat.NiTriStripsData()
	>>> block.set_triangles([(0,1,2),(2,1,3),(2,3,4)])
	>>> block.get_strips()
	[[0, 1, 2, 3, 4]]
	>>> block.get_triangles()
	[(0, 1, 2), (1, 3, 2), (2, 3, 4)]
	>>> block.set_strips([[1,0,1,2,3,4]])
	>>> block.get_strips()
	[[1, 0, 1, 2, 3, 4]]
	>>> block.get_triangles()
	[(0, 2, 1), (1, 2, 3), (2, 4, 3)]
	"""
	def get_triangles(self):
		return triangulate(self.points)

	def set_triangles(self, triangles, stitchstrips = False):
		self.set_strips(stripify(
			triangles, stitchstrips=stitchstrips))

	def get_strips(self):
		return [[i for i in strip] for strip in self.points]

	def set_strips(self, strips):
		# initialize strips array
		self.num_strips = len(strips)
		self.reset_field('strip_lengths')
		numtriangles = 0
		for i, strip in enumerate(strips):
			self.strip_lengths[i] = len(strip)
			numtriangles += len(strip) - 2
		self.num_triangles = numtriangles
		self.reset_field('points')
		self.has_points = (len(strips) > 0)

		# copy strips
		for i, strip in enumerate(strips):
			for j, idx in enumerate(strip):
				self.points[i][j] = idx

