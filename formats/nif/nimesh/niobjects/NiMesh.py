# START_GLOBALS
from itertools import chain
# END_GLOBALS

from generated.formats.nif.enums.MeshPrimitiveType import MeshPrimitiveType

class NiMesh:
# START_CLASS

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