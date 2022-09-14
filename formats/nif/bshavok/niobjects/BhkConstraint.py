# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS


class BhkConstraint:
# START_CLASS

	def get_transform_a_b(self, parent):
		"""Returns the transform of the first entity relative to the second
		entity. Root is simply a nif block that is a common parent to both
		blocks."""
		# check entities
		if self.num_entities != 2:
			raise ValueError(
				"cannot get tranform for constraint "
				"that hasn't exactly 2 entities")
		# find transform of entity A relative to entity B

		# find chains from parent to A and B entities
		chainA = parent.find_chain(self.entities[0])
		chainB = parent.find_chain(self.entities[1])
		# validate the chains
		assert(isinstance(chainA[-1], NifFormat.classes.BhkRigidBody))
		assert(isinstance(chainA[-2], NifFormat.classes.NiCollisionObject))
		assert(isinstance(chainA[-3], NifFormat.classes.NiNode))
		assert(isinstance(chainB[-1], NifFormat.classes.BhkRigidBody))
		assert(isinstance(chainB[-2], NifFormat.classes.NiCollisionObject))
		assert(isinstance(chainB[-3], NifFormat.classes.NiNode))
		# return the relative transform
		return (chainA[-3].get_transform(relative_to = parent)
				* chainB[-3].get_transform(relative_to = parent).get_inverse())
