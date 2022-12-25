# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS

class ControlledBlock:
# START_CLASS


	"""
	>>> from pyffi.formats.nif import NifFormat
	>>> link = NifFormat.ControlledBlock()
	>>> link.node_name_offset
	-1
	>>> link.set_node_name("Bip01")
	>>> link.node_name_offset
	0
	>>> link.get_node_name()
	'Bip01'
	>>> link.node_name
	'Bip01'
	>>> link.set_node_name("Bip01 Tail")
	>>> link.node_name_offset
	6
	>>> link.get_node_name()
	'Bip01 Tail'
	>>> link.node_name
	'Bip01 Tail'
	"""
	def _get_string(self, offset):
		"""A wrapper around string_palette.palette.get_string. Used by get_node_name
		etc. Returns the string at given offset."""
		if offset == -1:
			return ''

		if not self.string_palette:
			return ''

		return self.string_palette.palette.get_string(offset)

	def _add_string(self, text):
		"""Wrapper for string_palette.palette.add_string. Used by set_node_name etc.
		Returns offset of string added."""
		# create string palette if none exists yet
		if not self.string_palette:
			self.string_palette = NifFormat.classes.NiStringPalette(self.context)
		# add the string and return the offset
		return self.string_palette.palette.add_string(text)

	def get_node_name(self):
		"""Return the node name.

		>>> # a doctest
		>>> from pyffi.formats.nif import NifFormat
		>>> link = NifFormat.ControllerLink()
		>>> link.string_palette = NifFormat.NiStringPalette()
		>>> palette = link.string_palette.palette
		>>> link.node_name_offset = palette.add_string("Bip01")
		>>> link.get_node_name()
		'Bip01'

		>>> # another doctest
		>>> from pyffi.formats.nif import NifFormat
		>>> link = NifFormat.ControllerLink()
		>>> link.node_name = "Bip01"
		>>> link.get_node_name()
		'Bip01'
		"""
		# eg. ZT2
		if self.target_name:
			return self.target_name
		# eg. Fallout
		elif self.node_name:
			return self.node_name
		# eg. Loki (StringPalette)
		else:
			return self._get_string(self.node_name_offset)

	def set_node_name(self, text):
		self.target_name = text
		self.node_name = text
		self.node_name_offset = self._add_string(text)

	def get_property_type(self):
		if self.property_type:
			return self.property_type
		else:
			return self._get_string(self.property_type_offset)

	def set_property_type(self, text):
		self.property_type = text
		self.property_type_offset = self._add_string(text)

	def get_controller_type(self):
		if self.controller_type:
			return self.controller_type
		else:
			return self._get_string(self.controller_type_offset)

	def set_controller_type(self, text):
		self.controller_type = text
		self.controller_type_offset = self._add_string(text)

	def get_variable_1(self):
		if self.variable_1:
			return self.variable_1
		else:
			return self._get_string(self.variable_1_offset)

	def set_variable_1(self, text):
		self.variable_1 = text
		self.variable_1_offset = self._add_string(text)

	def get_variable_2(self):
		if self.variable_2:
			return self.variable_2
		else:
			return self._get_string(self.variable_2_offset)

	def set_variable_2(self, text):
		self.variable_2 = text
		self.variable_2_offset = self._add_string(text)
