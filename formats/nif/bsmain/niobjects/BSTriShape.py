class BSTriShape:
# START_CLASS

	def get_triangles(self):
		"""Return triangles"""
		if self.vertex_desc.vertex_attributes.skinned:
			# triangles are found in the partition
			triangles = []
			if self.skin:
				return self.skin.get_dismember_partitions[0]
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
