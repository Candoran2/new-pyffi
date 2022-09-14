# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS


class HkPackedNiTriStripsData:
# START_CLASS
	def apply_scale(self, scale):
		"""Apply scale factor on data."""
		if abs(scale - 1.0) < NifFormat.EPSILON:
			return
		for vert in self.vertices:
			vert.x *= scale
			vert.y *= scale
			vert.z *= scale
