class NiKeyframeData:
# START_CLASS
	def apply_scale(self, scale):
		"""Apply scale factor on data."""
		for key in self.translations.keys:
			key.value.x *= scale
			key.value.y *= scale
			key.value.z *= scale
			#key.forward.x *= scale
			#key.forward.y *= scale
			#key.forward.z *= scale
			#key.backward.x *= scale
			#key.backward.y *= scale
			#key.backward.z *= scale
			# what to do with TBC?

