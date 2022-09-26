# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS

class NiObjectNET:
# START_CLASS
	def add_extra_data(self, extrablock):
		"""Add block to extra data list and extra data chain. It is good practice
		to ensure that the extra data has empty next_extra_data field when adding it
		to avoid loops in the hierarchy."""
		# add to the list
		num_extra = self.num_extra_data_list
		self.num_extra_data_list = num_extra + 1
		self.reset_field("extra_data_list")
		self.extra_data_list[num_extra] = extrablock
		# add to the chain
		if not self.extra_data:
			self.extra_data = extrablock
		else:
			lastextra = self.extra_data
			while lastextra.next_extra_data:
				lastextra = lastextra.next_extra_data
			lastextra.next_extra_data = extrablock

	def remove_extra_data(self, extrablock):
		"""Remove block from extra data list and extra data chain.

		>>> from pyffi.formats.nif import NifFormat
		>>> block = NifFormat.NiNode()
		>>> block.num_extra_data_list = 3
		>>> block.extra_data_list.update_size()
		>>> extrablock = NifFormat.NiStringExtraData()
		>>> block.extra_data_list[1] = extrablock
		>>> block.remove_extra_data(extrablock)
		>>> [extra for extra in block.extra_data_list]
		[None, None]
		"""
		# remove from list
		new_extra_list = []
		for extraother in self.extra_data_list:
			if not extraother is extrablock:
				new_extra_list.append(extraother)
		self.num_extra_data_list = len(new_extra_list)
		self.reset_field("extra_data_list")
		for i, extraother in enumerate(new_extra_list):
			self.extra_data_list[i] = extraother
		# remove from chain
		if self.extra_data is extrablock:
			self.extra_data = extrablock.next_extra_data
		lastextra = self.extra_data
		while lastextra:
			if lastextra.next_extra_data is extrablock:
				lastextra.next_extra_data = lastextra.next_extra_data.next_extra_data
			lastextra = lastextra.next_extra_data

	def get_extra_datas(self):
		"""Get a list of all extra data blocks."""
		xtras = [xtra for xtra in self.extra_data_list]
		xtra = self.extra_data
		while xtra:
			if not xtra in self.extra_data_list:
				xtras.append(xtra)
			xtra = xtra.next_extra_data
		return xtras

	def set_extra_datas(self, extralist):
		"""Set all extra data blocks from given list (erases existing data).

		>>> from pyffi.formats.nif import NifFormat
		>>> node = NifFormat.NiNode()
		>>> extra1 = NifFormat.NiExtraData()
		>>> extra1.name = "hello"
		>>> extra2 = NifFormat.NiExtraData()
		>>> extra2.name = "world"
		>>> node.get_extra_datas()
		[]
		>>> node.set_extra_datas([extra1, extra2])
		>>> [extra.name for extra in node.get_extra_datas()]
		[b'hello', b'world']
		>>> [extra.name for extra in node.extra_data_list]
		[b'hello', b'world']
		>>> node.extra_data is extra1
		True
		>>> extra1.next_extra_data is extra2
		True
		>>> extra2.next_extra_data is None
		True
		>>> node.set_extra_datas([])
		>>> node.get_extra_datas()
		[]
		>>> # now set them the other way around
		>>> node.set_extra_datas([extra2, extra1])
		>>> [extra.name for extra in node.get_extra_datas()]
		[b'world', b'hello']
		>>> [extra.name for extra in node.extra_data_list]
		[b'world', b'hello']
		>>> node.extra_data is extra2
		True
		>>> extra2.next_extra_data is extra1
		True
		>>> extra1.next_extra_data is None
		True

		:param extralist: List of extra data blocks to add.
		:type extralist: ``list`` of L{NifFormat.NiExtraData}
		"""
		# set up extra data list
		self.num_extra_data_list = len(extralist)
		self.reset_field("extra_data_list")
		for i, extra in enumerate(extralist):
			self.extra_data_list[i] = extra
		# set up extra data chain
		# first, kill the current chain
		self.extra_data = None
		# now reconstruct it
		if extralist:
			self.extra_data = extralist[0]
			lastextra = self.extra_data
			for extra in extralist[1:]:
				lastextra.next_extra_data = extra
				lastextra = extra
			lastextra.next_extra_data = None

	def add_controller(self, ctrlblock):
		"""Add block to controller chain and set target of controller to self."""
		if not self.controller:
			self.controller = ctrlblock
		else:
			lastctrl = self.controller
			while lastctrl.next_controller:
				lastctrl = lastctrl.next_controller
			lastctrl.next_controller = ctrlblock
		# set the target of the controller
		ctrlblock.target = self

	def get_controllers(self):
		"""Get a list of all controllers."""
		ctrls = []
		ctrl = self.controller
		while ctrl:
			ctrls.append(ctrl)
			ctrl = ctrl.next_controller
		return ctrls

	def add_integer_extra_data(self, name, value):
		"""Add a particular extra integer data block."""
		extra = NifFormat.classes.NiIntegerExtraData()
		extra.name = name
		extra.integer_data = value
		self.add_extra_data(extra)
