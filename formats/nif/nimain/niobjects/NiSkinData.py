class NiSkinData:
# START_CLASS
	def get_transform(self):
		"""Return scale, rotation, and translation into a single 4x4 matrix."""
		return self.skin_transform.get_transform()

	def set_transform(self, mat):
		"""Set rotation, transform, and velocity."""
		self.skin_transform.set_transform(mat)

	def apply_scale(self, scale):
		"""Apply scale factor on data.

		>>> from pyffi.formats.nif import NifFormat
		>>> id44 = NifFormat.Matrix44()
		>>> id44.set_identity()
		>>> skelroot = NifFormat.NiNode()
		>>> skelroot.name = 'Scene Root'
		>>> skelroot.set_transform(id44)
		>>> bone1 = NifFormat.NiNode()
		>>> bone1.name = 'bone1'
		>>> bone1.set_transform(id44)
		>>> bone1.translation.x = 10
		>>> skelroot.add_child(bone1)
		>>> geom = NifFormat.NiTriShape()
		>>> geom.set_transform(id44)
		>>> skelroot.add_child(geom)
		>>> skininst = NifFormat.NiSkinInstance()
		>>> geom.skin_instance = skininst
		>>> skininst.skeleton_root = skelroot
		>>> skindata = NifFormat.NiSkinData()
		>>> skininst.data = skindata
		>>> skindata.set_transform(id44)
		>>> geom.add_bone(bone1, {})
		>>> geom.update_bind_position()
		>>> bone1.translation.x
		10.0
		>>> skindata.bone_list[0].skin_transform.translation.x
		-10.0
		>>> import pyffi.spells.nif.fix
		>>> import pyffi.spells.nif
		>>> data = NifFormat.Data()
		>>> data.roots = [skelroot]
		>>> toaster = pyffi.spells.nif.NifToaster()
		>>> toaster.scale = 0.1
		>>> pyffi.spells.nif.fix.SpellScale(data=data, toaster=toaster).recurse()
		pyffi.toaster:INFO:--- fix_scale ---
		pyffi.toaster:INFO:  scaling by factor 0.100000
		pyffi.toaster:INFO:  ~~~ NiNode [Scene Root] ~~~
		pyffi.toaster:INFO:	~~~ NiNode [bone1] ~~~
		pyffi.toaster:INFO:	~~~ NiTriShape [] ~~~
		pyffi.toaster:INFO:	  ~~~ NiSkinInstance [] ~~~
		pyffi.toaster:INFO:		~~~ NiSkinData [] ~~~
		>>> bone1.translation.x
		1.0
		>>> skindata.bone_list[0].skin_transform.translation.x
		-1.0
		"""

		self.skin_transform.translation.x *= scale
		self.skin_transform.translation.y *= scale
		self.skin_transform.translation.z *= scale

		for skindata in self.bone_list:
			skindata.skin_transform.translation.x *= scale
			skindata.skin_transform.translation.y *= scale
			skindata.skin_transform.translation.z *= scale
			skindata.bounding_sphere_offset.x *= scale
			skindata.bounding_sphere_offset.y *= scale
			skindata.bounding_sphere_offset.z *= scale
			skindata.bounding_sphere_radius *= scale
