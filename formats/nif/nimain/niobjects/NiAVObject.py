# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS

class NiAVObject:
# START_CLASS

	"""
	>>> from pyffi.formats.nif import NifFormat
	>>> node = NifFormat.NiNode()
	>>> prop1 = NifFormat.NiProperty()
	>>> prop1.name = "hello"
	>>> prop2 = NifFormat.NiProperty()
	>>> prop2.name = "world"
	>>> node.get_properties()
	[]
	>>> node.set_properties([prop1, prop2])
	>>> [prop.name for prop in node.get_properties()]
	[b'hello', b'world']
	>>> [prop.name for prop in node.properties]
	[b'hello', b'world']
	>>> node.set_properties([])
	>>> node.get_properties()
	[]
	>>> # now set them the other way around
	>>> node.set_properties([prop2, prop1])
	>>> [prop.name for prop in node.get_properties()]
	[b'world', b'hello']
	>>> [prop.name for prop in node.properties]
	[b'world', b'hello']
	>>> node.remove_property(prop2)
	>>> [prop.name for prop in node.properties]
	[b'hello']
	>>> node.add_property(prop2)
	>>> [prop.name for prop in node.properties]
	[b'hello', b'world']
	"""
	def add_property(self, prop):
		"""Add the given property to the property list.

		:param prop: The property block to add.
		:type prop: L{NifFormat.NiProperty}
		"""
		num_props = self.num_properties
		self.num_properties = num_props + 1
		self.properties.append(prop)

	def remove_property(self, prop):
		"""Remove the given property to the property list.

		:param prop: The property block to remove.
		:type prop: L{NifFormat.NiProperty}
		"""
		self.set_properties([otherprop for otherprop in self.get_properties()
							if not(otherprop is prop)])

	def get_properties(self):
		"""Return a list of the properties of the block.

		:return: The list of properties.
		:rtype: ``list`` of L{NifFormat.NiProperty}
		"""
		return [prop for prop in self.properties]

	def set_properties(self, proplist):
		"""Set the list of properties from the given list (destroys existing list).

		:param proplist: The list of property blocks to set.
		:type proplist: ``list`` of L{NifFormat.NiProperty}
		"""
		self.num_properties = len(proplist)
		self.reset_field("properties")
		for i, prop in enumerate(proplist):
			self.properties[i] = prop

	def get_transform(self, relative_to=None):
		"""Return scale, rotation, and translation into a single 4x4
		matrix, relative to the C{relative_to} block (which should be
		another NiAVObject connecting to this block). If C{relative_to} is
		``None``, then returns the transform stored in C{self}, or
		equivalently, the target is assumed to be the parent.

		:param relative_to: The block relative to which the transform must
			be calculated. If ``None``, the local transform is returned.
		"""
		m = NifFormat.classes.Matrix44()
		m.set_scale_rotation_translation(self.scale, self.rotation, self.translation)
		if not relative_to: return m
		# find chain from relative_to to self
		chain = relative_to.find_chain(self, block_type = NifFormat.classes.NiAVObject)
		if not chain:
			raise ValueError(
				'cannot find a chain of NiAVObject blocks '
				'between %s and %s.' % (self.name, relative_to.name))
		# and multiply with all transform matrices (not including relative_to)
		for block in reversed(chain[1:-1]):
			m *= block.get_transform()
		return m

	def set_transform(self, m):
		"""Set rotation, translation, and scale, from a 4x4 matrix.

		:param m: The matrix to which the transform should be set."""
		scale, rotation, translation = m.get_scale_rotation_translation()

		self.scale = scale

		self.rotation.m_11 = rotation.m_11
		self.rotation.m_12 = rotation.m_12
		self.rotation.m_13 = rotation.m_13
		self.rotation.m_21 = rotation.m_21
		self.rotation.m_22 = rotation.m_22
		self.rotation.m_23 = rotation.m_23
		self.rotation.m_31 = rotation.m_31
		self.rotation.m_32 = rotation.m_32
		self.rotation.m_33 = rotation.m_33

		self.translation.x = translation.x
		self.translation.y = translation.y
		self.translation.z = translation.z

	def apply_scale(self, scale):
		"""Apply scale factor on data.

		:param scale: The scale factor."""
		super().apply_scale(scale)
		# apply scale on translation
		self.translation.x *= scale
		self.translation.y *= scale
		self.translation.z *= scale
		# apply scale on bounding volume
		self.bounding_volume.apply_scale(scale)
