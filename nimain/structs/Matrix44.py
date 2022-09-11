import logging

from generated.formats.nif import EPSILON
from generated.formats.nif.nimain.structs.Matrix33 import Matrix33
from generated.formats.nif.nimain.structs.Vector3 import Vector3
from generated.formats.nif.nimain.structs.Vector4 import Vector4

class Matrix44:
# START_CLASS

	def __init__(self, context=None, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=True)
		self.set_defaults()

	def as_list(self):
		"""Return matrix as 4x4 list."""
		return [
			[self.m_11, self.m_12, self.m_13, self.m_14],
			[self.m_21, self.m_22, self.m_23, self.m_24],
			[self.m_31, self.m_32, self.m_33, self.m_34],
			[self.m_41, self.m_42, self.m_43, self.m_44]
			]

	def as_tuple(self):
		"""Return matrix as 4x4 tuple."""
		return (
			(self.m_11, self.m_12, self.m_13, self.m_14),
			(self.m_21, self.m_22, self.m_23, self.m_24),
			(self.m_31, self.m_32, self.m_33, self.m_34),
			(self.m_41, self.m_42, self.m_43, self.m_44)
			)

	def set_rows(self, row0, row1, row2, row3):
		"""Set matrix from rows."""
		self.m_11, self.m_12, self.m_13, self.m_14 = row0
		self.m_21, self.m_22, self.m_23, self.m_24 = row1
		self.m_31, self.m_32, self.m_33, self.m_34 = row2
		self.m_41, self.m_42, self.m_43, self.m_44 = row3

	def __str__(self):
		return(
			"[ %6.3f %6.3f %6.3f %6.3f ]\n"
			"[ %6.3f %6.3f %6.3f %6.3f ]\n"
			"[ %6.3f %6.3f %6.3f %6.3f ]\n"
			"[ %6.3f %6.3f %6.3f %6.3f ]\n"
			% (self.m_11, self.m_12, self.m_13, self.m_14,
			   self.m_21, self.m_22, self.m_23, self.m_24,
			   self.m_31, self.m_32, self.m_33, self.m_34,
			   self.m_41, self.m_42, self.m_43, self.m_44))

	def set_identity(self):
		"""Set to identity matrix."""
		self.m_11 = 1.0
		self.m_12 = 0.0
		self.m_13 = 0.0
		self.m_14 = 0.0
		self.m_21 = 0.0
		self.m_22 = 1.0
		self.m_23 = 0.0
		self.m_24 = 0.0
		self.m_31 = 0.0
		self.m_32 = 0.0
		self.m_33 = 1.0
		self.m_34 = 0.0
		self.m_41 = 0.0
		self.m_42 = 0.0
		self.m_43 = 0.0
		self.m_44 = 1.0

	def is_identity(self):
		"""Return ``True`` if the matrix is close to identity."""
		if (abs(self.m_11 - 1.0) > EPSILON
			or abs(self.m_12) > EPSILON
			or abs(self.m_13) > EPSILON
			or abs(self.m_14) > EPSILON
			or abs(self.m_21) > EPSILON
			or abs(self.m_22 - 1.0) > EPSILON
			or abs(self.m_23) > EPSILON
			or abs(self.m_24) > EPSILON
			or abs(self.m_31) > EPSILON
			or abs(self.m_32) > EPSILON
			or abs(self.m_33 - 1.0) > EPSILON
			or abs(self.m_34) > EPSILON
			or abs(self.m_41) > EPSILON
			or abs(self.m_42) > EPSILON
			or abs(self.m_43) > EPSILON
			or abs(self.m_44 - 1.0) > EPSILON):
			return False
		else:
			return True

	def get_copy(self):
		"""Create a copy of the matrix."""
		mat = Matrix44()
		mat.m_11 = self.m_11
		mat.m_12 = self.m_12
		mat.m_13 = self.m_13
		mat.m_14 = self.m_14
		mat.m_21 = self.m_21
		mat.m_22 = self.m_22
		mat.m_23 = self.m_23
		mat.m_24 = self.m_24
		mat.m_31 = self.m_31
		mat.m_32 = self.m_32
		mat.m_33 = self.m_33
		mat.m_34 = self.m_34
		mat.m_41 = self.m_41
		mat.m_42 = self.m_42
		mat.m_43 = self.m_43
		mat.m_44 = self.m_44
		return mat

	def get_matrix_33(self):
		"""Returns upper left 3x3 part."""
		m = Matrix33()
		m.m_11 = self.m_11
		m.m_12 = self.m_12
		m.m_13 = self.m_13
		m.m_21 = self.m_21
		m.m_22 = self.m_22
		m.m_23 = self.m_23
		m.m_31 = self.m_31
		m.m_32 = self.m_32
		m.m_33 = self.m_33
		return m

	def set_matrix_33(self, m):
		"""Sets upper left 3x3 part."""
		if not isinstance(m, Matrix33):
			raise TypeError('argument must be Matrix33')
		self.m_11 = m.m_11
		self.m_12 = m.m_12
		self.m_13 = m.m_13
		self.m_21 = m.m_21
		self.m_22 = m.m_22
		self.m_23 = m.m_23
		self.m_31 = m.m_31
		self.m_32 = m.m_32
		self.m_33 = m.m_33

	def get_translation(self):
		"""Returns lower left 1x3 part."""
		t = Vector3()
		t.x = self.m_41
		t.y = self.m_42
		t.z = self.m_43
		return t

	def set_translation(self, translation):
		"""Returns lower left 1x3 part."""
		if not isinstance(translation, Vector3):
			raise TypeError('argument must be Vector3')
		self.m_41 = translation.x
		self.m_42 = translation.y
		self.m_43 = translation.z

	def is_scale_rotation_translation(self):
		if not self.get_matrix_33().is_scale_rotation(): return False
		if abs(self.m_14) > EPSILON: return False
		if abs(self.m_24) > EPSILON: return False
		if abs(self.m_34) > EPSILON: return False
		if abs(self.m_44 - 1.0) > EPSILON: return False
		return True

	def get_scale_rotation_translation(self):
		rotscl = self.get_matrix_33()
		scale = rotscl.get_scale()
		rot = rotscl / scale
		trans = self.get_translation()
		return (scale, rot, trans)

	def get_scale_quat_translation(self):
		rotscl = self.get_matrix_33()
		scale, quat = rotscl.get_scale_quat()
		trans = self.get_translation()
		return (scale, quat, trans)

	def set_scale_rotation_translation(self, scale, rotation, translation):
		if not isinstance(scale, (float, int)):
			raise TypeError('scale must be float')
		if not isinstance(rotation, Matrix33):
			raise TypeError('rotation must be Matrix33')
		if not isinstance(translation, Vector3):
			raise TypeError('translation must be Vector3')

		if not rotation.is_rotation():
			logger = logging.getLogger("generated.formats.nif.nimain.struct.matrix44")
			mat = rotation * rotation.get_transpose()
			idmat = Matrix33()
			idmat.set_identity()
			error = (mat - idmat).sup_norm()
			logger.warning("improper rotation matrix (error is %f)" % error)
			logger.debug("  matrix =")
			for line in str(rotation).split("\n"):
				logger.debug("	%s" % line)
			logger.debug("  its determinant = %f" % rotation.get_determinant())
			logger.debug("  matrix * matrix^T =")
			for line in str(mat).split("\n"):
				logger.debug("	%s" % line)

		self.m_14 = 0.0
		self.m_24 = 0.0
		self.m_34 = 0.0
		self.m_44 = 1.0

		self.set_matrix_33(rotation * scale)
		self.set_translation(translation)

	def get_inverse(self, fast=True):
		"""Calculates inverse (fast assumes is_scale_rotation_translation is True)."""
		def adjoint(m, ii, jj):
			result = []
			for i, row in enumerate(m):
				if i == ii: continue
				result.append([])
				for j, x in enumerate(row):
					if j == jj: continue
					result[-1].append(x)
			return result
		def determinant(m):
			if len(m) == 2:
				return m[0][0]*m[1][1] - m[1][0]*m[0][1]
			result = 0.0
			for i in range(len(m)):
				det = determinant(adjoint(m, i, 0))
				if i & 1:
					result -= m[i][0] * det
				else:
					result += m[i][0] * det
			return result

		if fast:
			m = self.get_matrix_33().get_inverse()
			t = -(self.get_translation() * m)

			n = Matrix44()
			n.m_14 = 0.0
			n.m_24 = 0.0
			n.m_34 = 0.0
			n.m_44 = 1.0
			n.set_matrix_33(m)
			n.set_translation(t)
			return n
		else:
			m = self.as_list()
			nn = [[0.0 for i in range(4)] for j in range(4)]
			det = determinant(m)
			if abs(det) < EPSILON:
				raise ZeroDivisionError('cannot invert matrix:\n%s'%self)
			for i in range(4):
				for j in range(4):
					if (i+j) & 1:
						nn[j][i] = -determinant(adjoint(m, i, j)) / det
					else:
						nn[j][i] = determinant(adjoint(m, i, j)) / det
			n = Matrix44()
			n.set_rows(*nn)
			return n

	def __mul__(self, x):
		if isinstance(x, (float, int)):
			m = Matrix44()
			m.m_11 = self.m_11 * x
			m.m_12 = self.m_12 * x
			m.m_13 = self.m_13 * x
			m.m_14 = self.m_14 * x
			m.m_21 = self.m_21 * x
			m.m_22 = self.m_22 * x
			m.m_23 = self.m_23 * x
			m.m_24 = self.m_24 * x
			m.m_31 = self.m_31 * x
			m.m_32 = self.m_32 * x
			m.m_33 = self.m_33 * x
			m.m_34 = self.m_34 * x
			m.m_41 = self.m_41 * x
			m.m_42 = self.m_42 * x
			m.m_43 = self.m_43 * x
			m.m_44 = self.m_44 * x
			return m
		elif isinstance(x, Vector3):
			raise TypeError("matrix*vector not supported; please use left multiplication (vector*matrix)")
		elif isinstance(x, Vector4):
			raise TypeError("matrix*vector not supported; please use left multiplication (vector*matrix)")
		elif isinstance(x, Matrix44):
			m = Matrix44()
			m.m_11 = self.m_11 * x.m_11  +  self.m_12 * x.m_21  +  self.m_13 * x.m_31  +  self.m_14 * x.m_41
			m.m_12 = self.m_11 * x.m_12  +  self.m_12 * x.m_22  +  self.m_13 * x.m_32  +  self.m_14 * x.m_42
			m.m_13 = self.m_11 * x.m_13  +  self.m_12 * x.m_23  +  self.m_13 * x.m_33  +  self.m_14 * x.m_43
			m.m_14 = self.m_11 * x.m_14  +  self.m_12 * x.m_24  +  self.m_13 * x.m_34  +  self.m_14 * x.m_44
			m.m_21 = self.m_21 * x.m_11  +  self.m_22 * x.m_21  +  self.m_23 * x.m_31  +  self.m_24 * x.m_41
			m.m_22 = self.m_21 * x.m_12  +  self.m_22 * x.m_22  +  self.m_23 * x.m_32  +  self.m_24 * x.m_42
			m.m_23 = self.m_21 * x.m_13  +  self.m_22 * x.m_23  +  self.m_23 * x.m_33  +  self.m_24 * x.m_43
			m.m_24 = self.m_21 * x.m_14  +  self.m_22 * x.m_24  +  self.m_23 * x.m_34  +  self.m_24 * x.m_44
			m.m_31 = self.m_31 * x.m_11  +  self.m_32 * x.m_21  +  self.m_33 * x.m_31  +  self.m_34 * x.m_41
			m.m_32 = self.m_31 * x.m_12  +  self.m_32 * x.m_22  +  self.m_33 * x.m_32  +  self.m_34 * x.m_42
			m.m_33 = self.m_31 * x.m_13  +  self.m_32 * x.m_23  +  self.m_33 * x.m_33  +  self.m_34 * x.m_43
			m.m_34 = self.m_31 * x.m_14  +  self.m_32 * x.m_24  +  self.m_33 * x.m_34  +  self.m_34 * x.m_44
			m.m_41 = self.m_41 * x.m_11  +  self.m_42 * x.m_21  +  self.m_43 * x.m_31  +  self.m_44 * x.m_41
			m.m_42 = self.m_41 * x.m_12  +  self.m_42 * x.m_22  +  self.m_43 * x.m_32  +  self.m_44 * x.m_42
			m.m_43 = self.m_41 * x.m_13  +  self.m_42 * x.m_23  +  self.m_43 * x.m_33  +  self.m_44 * x.m_43
			m.m_44 = self.m_41 * x.m_14  +  self.m_42 * x.m_24  +  self.m_43 * x.m_34  +  self.m_44 * x.m_44
			return m
		else:
			raise TypeError("do not know how to multiply Matrix44 with %s"%x.__class__)

	def __div__(self, x):
		if isinstance(x, (float, int)):
			m = Matrix44()
			m.m_11 = self.m_11 / x
			m.m_12 = self.m_12 / x
			m.m_13 = self.m_13 / x
			m.m_14 = self.m_14 / x
			m.m_21 = self.m_21 / x
			m.m_22 = self.m_22 / x
			m.m_23 = self.m_23 / x
			m.m_24 = self.m_24 / x
			m.m_31 = self.m_31 / x
			m.m_32 = self.m_32 / x
			m.m_33 = self.m_33 / x
			m.m_34 = self.m_34 / x
			m.m_41 = self.m_41 / x
			m.m_42 = self.m_42 / x
			m.m_43 = self.m_43 / x
			m.m_44 = self.m_44 / x
			return m
		else:
			raise TypeError("do not know how to divide Matrix44 by %s"%x.__class__)

	# py3k
	__truediv__ = __div__

	def __rmul__(self, x):
		if isinstance(x, (float, int)):
			return self * x
		else:
			raise TypeError("do not know how to multiply %s with Matrix44"%x.__class__)

	def __eq__(self, m):
		if isinstance(m, type(None)):
			return False
		if not isinstance(m, Matrix44):
			raise TypeError("do not know how to compare Matrix44 and %s"%m.__class__)
		if abs(self.m_11 - m.m_11) > EPSILON: return False
		if abs(self.m_12 - m.m_12) > EPSILON: return False
		if abs(self.m_13 - m.m_13) > EPSILON: return False
		if abs(self.m_14 - m.m_14) > EPSILON: return False
		if abs(self.m_21 - m.m_21) > EPSILON: return False
		if abs(self.m_22 - m.m_22) > EPSILON: return False
		if abs(self.m_23 - m.m_23) > EPSILON: return False
		if abs(self.m_24 - m.m_24) > EPSILON: return False
		if abs(self.m_31 - m.m_31) > EPSILON: return False
		if abs(self.m_32 - m.m_32) > EPSILON: return False
		if abs(self.m_33 - m.m_33) > EPSILON: return False
		if abs(self.m_34 - m.m_34) > EPSILON: return False
		if abs(self.m_41 - m.m_41) > EPSILON: return False
		if abs(self.m_42 - m.m_42) > EPSILON: return False
		if abs(self.m_43 - m.m_43) > EPSILON: return False
		if abs(self.m_44 - m.m_44) > EPSILON: return False
		return True

	def __ne__(self, m):
		return not self.__eq__(m)

	def __add__(self, x):
		if isinstance(x, (Matrix44)):
			m = Matrix44()
			m.m_11 = self.m_11 + x.m_11
			m.m_12 = self.m_12 + x.m_12
			m.m_13 = self.m_13 + x.m_13
			m.m_14 = self.m_14 + x.m_14
			m.m_21 = self.m_21 + x.m_21
			m.m_22 = self.m_22 + x.m_22
			m.m_23 = self.m_23 + x.m_23
			m.m_24 = self.m_24 + x.m_24
			m.m_31 = self.m_31 + x.m_31
			m.m_32 = self.m_32 + x.m_32
			m.m_33 = self.m_33 + x.m_33
			m.m_34 = self.m_34 + x.m_34
			m.m_41 = self.m_41 + x.m_41
			m.m_42 = self.m_42 + x.m_42
			m.m_43 = self.m_43 + x.m_43
			m.m_44 = self.m_44 + x.m_44
			return m
		elif isinstance(x, (int, float)):
			m = Matrix44()
			m.m_11 = self.m_11 + x
			m.m_12 = self.m_12 + x
			m.m_13 = self.m_13 + x
			m.m_14 = self.m_14 + x
			m.m_21 = self.m_21 + x
			m.m_22 = self.m_22 + x
			m.m_23 = self.m_23 + x
			m.m_24 = self.m_24 + x
			m.m_31 = self.m_31 + x
			m.m_32 = self.m_32 + x
			m.m_33 = self.m_33 + x
			m.m_34 = self.m_34 + x
			m.m_41 = self.m_41 + x
			m.m_42 = self.m_42 + x
			m.m_43 = self.m_43 + x
			m.m_44 = self.m_44 + x
			return m
		else:
			raise TypeError("do not know how to add Matrix44 and %s"%x.__class__)

	def __sub__(self, x):
		if isinstance(x, (Matrix44)):
			m = Matrix44()
			m.m_11 = self.m_11 - x.m_11
			m.m_12 = self.m_12 - x.m_12
			m.m_13 = self.m_13 - x.m_13
			m.m_14 = self.m_14 - x.m_14
			m.m_21 = self.m_21 - x.m_21
			m.m_22 = self.m_22 - x.m_22
			m.m_23 = self.m_23 - x.m_23
			m.m_24 = self.m_24 - x.m_24
			m.m_31 = self.m_31 - x.m_31
			m.m_32 = self.m_32 - x.m_32
			m.m_33 = self.m_33 - x.m_33
			m.m_34 = self.m_34 - x.m_34
			m.m_41 = self.m_41 - x.m_41
			m.m_42 = self.m_42 - x.m_42
			m.m_43 = self.m_43 - x.m_43
			m.m_44 = self.m_44 - x.m_44
			return m
		elif isinstance(x, (int, float)):
			m = Matrix44()
			m.m_11 = self.m_11 - x
			m.m_12 = self.m_12 - x
			m.m_13 = self.m_13 - x
			m.m_14 = self.m_14 - x
			m.m_21 = self.m_21 - x
			m.m_22 = self.m_22 - x
			m.m_23 = self.m_23 - x
			m.m_24 = self.m_24 - x
			m.m_31 = self.m_31 - x
			m.m_32 = self.m_32 - x
			m.m_33 = self.m_33 - x
			m.m_34 = self.m_34 - x
			m.m_41 = self.m_41 - x
			m.m_42 = self.m_42 - x
			m.m_43 = self.m_43 - x
			m.m_44 = self.m_44 - x
			return m
		else:
			raise TypeError("do not know how to substract Matrix44 and %s"
							% x.__class__)

	def sup_norm(self):
		"""Calculate supremum norm of matrix (maximum absolute value of all
		entries)."""
		return max(max(abs(elem) for elem in row)
				   for row in self.as_list())
