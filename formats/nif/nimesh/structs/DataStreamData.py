# START_GLOBALS
from math import prod

from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.nif.bitfields.ComponentFormat import ComponentFormat
# END_GLOBALS


class DataStreamData:

# START_CLASS

	def __new__(cls, context, arg, template, set_default=True):
		el_width = cls.size_from_components(template)
		if el_width == 0:
			arr_length = 0
		else:
			arr_length = arg // el_width
		return Array(context, 0, None, (arr_length,), cls.struct_from_components(template))

	@classmethod
	def from_stream(cls, stream, context, arg, template):
		el_width = cls.size_from_components(template)
		return Array.from_stream(stream, context, 0, None, (arg // el_width,), cls.struct_from_components(template))

	@classmethod
	def to_stream(cls, instance, stream, context, arg, template):
		el_width = cls.size_from_components(template)
		return Array.to_stream(instance, stream, context, 0, None, (arg // el_width,), cls.struct_from_components(template))

	@classmethod
	def validate_instance(cls, instance, context, arg, template):
		assert len(instance) == arg
		# check the dtype later
		# check the individual fields later
		pass

	get_field = None
	_get_filtered_attribute_list = None

	@staticmethod
	def size_from_components(components):
		if len(components) > 0:
			return sum([ComponentFormat.get_component_size(component) for component in components])
		else:
			return 0

	@classmethod
	def struct_from_components(cls, components):
		component_structs = [ComponentFormat.struct_from_format(component) for component in components]
		if len(component_structs) == 1:
			return component_structs[0]
		else:
			# create a struct representing the components given as input to allow reading/writing
			# the created fields are called cx, where x is the index for that component (0-based)
			field_names = [f"c{i}" for i in range(len(component_structs))]


			class created_struct(BaseStruct):

				__name__  = str(tuple(component.__name__ for component in component_structs))

				_attribute_list = [(f_name, f_type, (0, None), (False, None), None) for f_name, f_type in zip(field_names, component_structs)]

				@staticmethod
				def _get_filtered_attribute_list(instance, include_abstract=True):
					for f_name, f_type in zip(field_names, component_structs):
						yield f_name, f_type, (0, None), (False, None)


			return created_struct
