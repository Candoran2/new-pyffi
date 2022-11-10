# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS

class BSDynamicTriShape:
# START_CLASS

	def apply_scale(self, scale):
		if abs(scale - 1.0) <= NifFormat.EPSILON: return
		super().apply_scale(scale)
		for vertex in self.vertices:
			vertex.x *= scale
			vertex.y *= scale
			vertex.z *= scale
