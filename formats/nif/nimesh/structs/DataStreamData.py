from generated.formats.nif.imports import name_type_map
# START_GLOBALS

from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.nif.enums.ComponentFormat import ComponentFormat
# END_GLOBALS


class DataStreamData:

# START_CLASS

	def __new__(cls, context, arg, template=None, set_default=True):
		el_width = cls.size_from_components(arg[1])
		if el_width == 0:
			arr_length = 0
		else:
			arr_length = arg[0] // el_width
		return Array(context, 0, None, (arr_length,), cls.struct_from_components(arg[1]))

	@classmethod
	def from_stream(cls, stream, context, arg, template=None):
		el_width = cls.size_from_components(arg[1])
		return Array.from_stream(stream, context, 0, None, (arg[0] // el_width,), cls.struct_from_components(arg[1]))

	@classmethod
	def to_stream(cls, instance, stream, context, arg, template=None):
		el_width = cls.size_from_components(arg[1])
		return Array.to_stream(instance, stream, context, 0, None, (arg[0] // el_width,), cls.struct_from_components(arg[1]))

	@staticmethod
	def get_size(instance, context, arg=0, template=None):
		return arg[0]

	@classmethod
	def validate_instance(cls, instance, context, arg, template=None):
		assert len(instance) == arg[0] // cls.size_from_components(arg[1])
		# check the dtype later
		# check the individual fields later
		pass

	get_field = None
	_get_filtered_attribute_list = None

	@staticmethod
	def size_from_components(components):
		return sum([ComponentFormat.get_component_size(component) for component in components])

	@classmethod
	def struct_from_components(cls, components):
		component_structs = [ComponentFormat.struct_for_format(component) for component in components]
		if len(component_structs) == 1:
			return component_structs[0]
		else:
			# create a struct representing the components given as input to allow reading/writing
			# the created fields are called cx, where x is the index for that component (0-based)
			field_names = [f"c{i}" for i in range(len(component_structs))]


			class created_struct(BaseStruct):

				__name__  = str(tuple(component.__name__ for component in component_structs))

				@staticmethod
				def _get_attribute_list():
					for f_name, f_type in zip(field_names, component_structs):
						yield f_name, f_type, (0, None), (False, None), (None, None)

				@staticmethod
				def _get_filtered_attribute_list(instance, include_abstract=True):
					for f_name, f_type in zip(field_names, component_structs):
						yield f_name, f_type, (0, None), (False, None)

			created_struct.init_attributes()

			return created_struct
