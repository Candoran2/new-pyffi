# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS

class BSTriShape:
# START_CLASS

	def apply_scale(self, scale):
		if abs(scale - 1.0) <= NifFormat.EPSILON: return
		super().apply_scale(scale)
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
