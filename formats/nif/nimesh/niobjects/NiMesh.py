# START_GLOBALS
from itertools import chain


from generated.utils.tristrip import triangulate
import generated.formats.nif as NifFormat
# END_GLOBALS

import name_type_map

class NiMesh:
# START_CLASS

	def apply_scale(self, scale):
		"""Apply scale factor on data."""
		if abs(scale - 1.0) <= NifFormat.EPSILON: return
		super().apply_scale(scale)
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

	def geomdata_by_name(self, name, sep_datastreams=True, sep_regions=False):
		"""Returns a list of all matching info from the nimesh datastreams. If multiple match, then they are sorted by 
		the index. Will always return a list.
		:param name: the component name to search for
		:type name: str
		:param sep_datastreams: whether to return a list of all matching data separated by stream, or one single list
		:type sep_datastreams: bool, optional"
		:param sep_regions: whether to subdivide datastreams in lists of regions
		:type sep_regions: bool, optional

		:return: A list of the matching data, format depends on the settings
		:rtype: list"""
		geom_data = []
		indices = []
		for meshdata in self.datastreams:
			for i, semanticdata in enumerate(meshdata.component_semantics):
				if semanticdata.name == name:
					indices.append(semanticdata.index)
					datastream = meshdata.stream
					streamdata = datastream.data
					if meshdata.num_components == 1:
						found_data = streamdata
					else:
						found_data = [getattr(row_struct, f"c{i}") for row_struct in streamdata]
					if sep_regions == True:
						found_data = [found_data[region.start_index:region.start_index + region.num_indices]
									  for region in datastream.regions]
					geom_data.append(found_data)
		sorted_data_zip = sorted(zip(geom_data, indices), key=lambda x: x[1])
		sorted_data = [data for data, i in sorted_data_zip]
		if not sep_datastreams:
			sorted_data = list(chain.from_iterable(sorted_data))
		return sorted_data

	def get_triangles(self):
		# sep_datastreams is allowed only under the assumption that there will be only one datastream containing triangles
		vertices = []
		vertices.extend(self.geomdata_by_name("POSITION", sep_datastreams=False, sep_regions=True))
		vertices.extend(self.geomdata_by_name("POSITION_BP", sep_datastreams=False, sep_regions=True))
		triangles = self.geomdata_by_name("INDEX", sep_datastreams=False, sep_regions=True)
		# resolve the regions into indices referring to the bare vertex index (as though there are no regions)
		if len(vertices) > 0:
			# skip the first region (if it exists), because adding 0 to the index is pointless
			offset = len(vertices[0])
		for v_region, t_region in zip(vertices[1:], triangles[1:]):
			# assume that every region starts where the previous ends
			for i in range(len(t_region)):
				t_region[i] += offset
			offset += len(v_region)

		def tris_from_tri_indices(indices):
			return [[subtriangles[i:i + 3] for i in range(0, len(subtriangles) - 2, 3)] for subtriangles in indices]

		primitive_type = self.primitive_type
		if primitive_type == name_type_map['MeshPrimitiveType'].MESH_PRIMITIVE_TRIANGLES:
			# based on assasin.nif, the components for a triangle datastream are single indices, meant to be 
			# interpreted three at a time, rather than the more obvious components with three ints
			triangles = tris_from_tri_indices(triangles)
		elif primitive_type == name_type_map['MeshPrimitiveType'].MESH_PRIMITIVE_TRISTRIPS:
			if self.context.version == 0x14060500:
				# Epic Mickey 2 primitive tristrips appear to be flattened normal triangles
				triangles = tris_from_tri_indices(triangles)
			else:
				triangles = [triangulate(triangles)]
		else:
			raise NotImplementedError(f"get_triangles is not implemented for primitive type {primitive_type}")
		triangles = list(chain.from_iterable(triangles))
		return triangles
