class NiMaterialProperty:
# START_CLASS
	def is_interchangeable(self, other):
		"""Are the two material blocks interchangeable?"""
		specialnames = (b"envmap2", b"envmap", b"skin", b"hair",
						b"dynalpha", b"hidesecret", b"lava")
		if self.__class__ is not other.__class__:
			return False
		if (self.name.lower() in specialnames
			or other.name.lower() in specialnames):
			# do not ignore name
			return self.get_hash() == other.get_hash()
		else:
			# ignore name
			return self.get_hash()[1:] == other.get_hash()[1:]