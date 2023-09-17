class NiCollisionData:
# START_CLASS

	def apply_scale(self, scale):
		super().apply_scale(scale)
		if hasattr(self, 'bounding_volume'):
			self.bounding_volume.apply_scale(scale)