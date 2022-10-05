class NiSkinPartition:
# START_CLASS

	def apply_scale(self, scale):
		for v_data in self.vertex_data:
			v = v_data.vertex
			v.x *= scale
			v.y *= scale
			v.z *= scale