class BSDismemberSkinInstance:
# START_CLASS

	def get_dismember_partitions(self):
		"""Return triangles and body part indices."""
		triangles = []
		trianglepartmap = []
		for bodypart, skinpartblock in zip(
			self.partitions, self.skin_partition.partitions):
			if self.skin_partition.vertex_desc:
				# use as proxy for SSE skinpartition, whose triangles don't use the vertex map
				part_triangles = skinpartblock.triangles
			else:
				part_triangles = list(skinpartblock.get_mapped_triangles())
			triangles.extend(part_triangles)
			trianglepartmap += [bodypart.body_part] * len(part_triangles)
		return triangles, trianglepartmap
