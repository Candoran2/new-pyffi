class NiMaterialColorController:
# START_CLASS
	def get_target_color(self):
		"""Get target color (works for all nif versions)."""
		return ((self.flags >> 4) & 7) | self.target_color

	def set_target_color(self, target_color):
		"""Set target color (works for all nif versions)."""
		self.flags |= (target_color & 7) << 4
		self.target_color = target_color

