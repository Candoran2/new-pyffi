class BhkRigidBody:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor <scale> on data."""
		# apply scale on transform
		self.rigid_body_info.translation.x *= scale
		self.rigid_body_info.translation.y *= scale
		self.rigid_body_info.translation.z *= scale

		# apply scale on center of gravity
		self.rigid_body_info.center.x *= scale
		self.rigid_body_info.center.y *= scale
		self.rigid_body_info.center.z *= scale

		# apply scale on inertia tensor
		self.rigid_body_info.inertia_tensor.m_11 *= (scale ** 2)
		self.rigid_body_info.inertia_tensor.m_12 *= (scale ** 2)
		self.rigid_body_info.inertia_tensor.m_13 *= (scale ** 2)
		self.rigid_body_info.inertia_tensor.m_14 *= (scale ** 2)
		self.rigid_body_info.inertia_tensor.m_21 *= (scale ** 2)
		self.rigid_body_info.inertia_tensor.m_22 *= (scale ** 2)
		self.rigid_body_info.inertia_tensor.m_23 *= (scale ** 2)
		self.rigid_body_info.inertia_tensor.m_24 *= (scale ** 2)
		self.rigid_body_info.inertia_tensor.m_31 *= (scale ** 2)
		self.rigid_body_info.inertia_tensor.m_32 *= (scale ** 2)
		self.rigid_body_info.inertia_tensor.m_33 *= (scale ** 2)
		self.rigid_body_info.inertia_tensor.m_34 *= (scale ** 2)

	def update_mass_center_inertia(self, density=1, solid=True, mass=None):
		"""Look at all the objects under this rigid body and update the mass,
		center of gravity, and inertia tensor accordingly. If the C{mass} parameter
		is given then the C{density} argument is ignored."""
		if not mass is None:
			density = 1

		calc_mass, center, inertia = self.get_shape_mass_center_inertia(
			density=density, solid=solid)

		self.mass = calc_mass
		self.center.x, self.center.y, self.center.z = center
		self.rigid_body_info.inertia_tensor.m_11 = inertia[0][0]
		self.rigid_body_info.inertia_tensor.m_12 = inertia[0][1]
		self.rigid_body_info.inertia_tensor.m_13 = inertia[0][2]
		self.rigid_body_info.inertia_tensor.m_14 = 0
		self.rigid_body_info.inertia_tensor.m_21 = inertia[1][0]
		self.rigid_body_info.inertia_tensor.m_22 = inertia[1][1]
		self.rigid_body_info.inertia_tensor.m_23 = inertia[1][2]
		self.rigid_body_info.inertia_tensor.m_24 = 0
		self.rigid_body_info.inertia_tensor.m_31 = inertia[2][0]
		self.rigid_body_info.inertia_tensor.m_32 = inertia[2][1]
		self.rigid_body_info.inertia_tensor.m_33 = inertia[2][2]
		self.rigid_body_info.inertia_tensor.m_34 = 0

		if not mass is None:
			mass_correction = mass / calc_mass if calc_mass != 0 else 1
			self.mass = mass
			self.rigid_body_info.inertia_tensor.m_11 *= mass_correction
			self.rigid_body_info.inertia_tensor.m_12 *= mass_correction
			self.rigid_body_info.inertia_tensor.m_13 *= mass_correction
			self.rigid_body_info.inertia_tensor.m_14 *= mass_correction
			self.rigid_body_info.inertia_tensor.m_21 *= mass_correction
			self.rigid_body_info.inertia_tensor.m_22 *= mass_correction
			self.rigid_body_info.inertia_tensor.m_23 *= mass_correction
			self.rigid_body_info.inertia_tensor.m_24 *= mass_correction
			self.rigid_body_info.inertia_tensor.m_31 *= mass_correction
			self.rigid_body_info.inertia_tensor.m_32 *= mass_correction
			self.rigid_body_info.inertia_tensor.m_33 *= mass_correction
			self.rigid_body_info.inertia_tensor.m_34 *= mass_correction

