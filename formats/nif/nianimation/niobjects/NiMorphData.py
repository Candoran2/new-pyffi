class NiMorphData:
# START_CLASS
	def apply_scale(self, scale):
		"""Apply scale factor on data."""
		for morph in self.morphs:
			for v in morph.vectors:
				v.x *= scale
				v.y *= scale
				v.z *= scale
