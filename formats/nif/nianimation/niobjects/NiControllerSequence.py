class NiControllerSequence:
# START_CLASS
	def add_controlled_block(self):
		"""Create new controlled block, and return it.

		>>> seq = NifFormat.NiControllerSequence()
		>>> seq.num_controlled_blocks
		0
		>>> ctrlblock = seq.add_controlled_block()
		>>> seq.num_controlled_blocks
		1
		>>> isinstance(ctrlblock, NifFormat.ControllerLink)
		True
		"""
		# add to the list
		num_blocks = self.num_controlled_blocks
		self.num_controlled_blocks = num_blocks + 1
		self.controlled_blocks.update_size()
		return self.controlled_blocks[-1]
