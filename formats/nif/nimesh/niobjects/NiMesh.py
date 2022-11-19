# START_GLOBALS
from itertools import chain

import generated.formats.nif as NifFormat
# END_GLOBALS

from generated.formats.nif.enums.MeshPrimitiveType import MeshPrimitiveType

class NiMesh:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor on data."""
		if abs(scale - 1.0) <= NifFormat.EPSILON: return
		position_datas = []
		position_datas.extend(self.geomdata_by_name("POSITION"))
		position_datas.extend(self.geomdata_by_name("POSITION_BP"))
		for data in position_datas:
			for position in data:
				for i in range(len(position)):
					position[i] *= scale
		if self.has_extra_em_data:
			for matrix in self.extra_em_data.bone_transforms:
				matrix.m_14 *= scale
				matrix.m_24 *= scale
				matrix.m_34 *= scale

	def is_skin(self):
		if self.has_extra_em_data:
			return self.extra_em_data.num_weights > 0
		else:
			# not sure this is the right type of semanticdata, but use for now
			return len(self.geomdata_by_name("BONE_PALETTE")) > 0

	def geomdata_by_name(self, name):
		"""Returns a list of all matching info from the nimesh datastreams. If multiple match, then they are sorted by 
		the index"""
		geom_data = []
		indices = []
		for meshdata in self.datastreams:
			for i, semanticdata in enumerate(meshdata.component_semantics):
				if semanticdata.name == name:
					indices.append(semanticdata.index)
					datastream = meshdata.stream.data
					if meshdata.num_components == 1:
						found_data = datastream
					else:
						found_data = [getattr(row_struct, f"c{i}") for row_struct in datastream]
					geom_data.append(found_data)
		sorted_data_zip = sorted(zip(geom_data, indices), key=lambda x: x[1])
		return [data for data, i in sorted_data_zip]

	def get_triangles(self):
		triangles = self.geomdata_by_name("INDEX")
		primitive_type = self.primitive_type
		if primitive_type == MeshPrimitiveType.MESH_PRIMITIVE_TRIANGLES:
			# based on assasin.nif, the components for a triangle datastream are single indices, meant to be 
			# interpreted three at a time, rather than the more obvious components with three ints
			triangles = [[subtriangles[i:i + 3] for i in range(0, len(subtriangles) - 2, 3)] for subtriangles in triangles]
		elif primitive_type == MeshPrimitiveType.MESH_PRIMITIVE_TRISTRIPS:
			# in spite of the name, Epic Mickey 2 primitive tristrips appear to be flattened normal triangles
			triangles = [[subtriangles[i:i + 3] for i in range(0, len(subtriangles) - 2, 3)] for subtriangles in triangles]
		else:
			raise NotImplementedError(f"get_triangles is not implemented for primitive type {primitive_type}")
		triangles = list(chain.from_iterable(triangles))
		return triangles