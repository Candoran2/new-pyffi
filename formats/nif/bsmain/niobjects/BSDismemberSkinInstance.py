class BSDismemberSkinInstance:
# START_CLASS

	def get_dismember_partitions(self):
		"""Return triangles and body part indices."""
		triangles = []
		trianglepartmap = []
		for bodypart, skinpartblock in zip(
			self.partitions, self.skin_partition.skin_partition_blocks):
			part_triangles = list(skinpartblock.get_mapped_triangles())
			triangles += part_triangles
			trianglepartmap += [bodypart.body_part] * len(part_triangles)
		return triangles, trianglepartmap
