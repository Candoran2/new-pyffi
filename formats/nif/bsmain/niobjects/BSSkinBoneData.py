# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS

class BSSkinBoneData:
# START_CLASS

	def apply_scale(self, scale):
		if abs(scale - 1.0) <= NifFormat.EPSILON: return
		super().apply_scale(scale)
		for bone in self.bone_list:
			bone.bounding_sphere.apply_scale(scale)
			bone.translation.x *= scale
			bone.translation.y *= scale
			bone.translation.z *= scale
