# START_GLOBALS
import itertools
# END_GLOBALS


class NiBSplineData:
# START_CLASS
	"""
	>>> # a doctest
	>>> from pyffi.formats.nif import NifFormat
	>>> block = NifFormat.NiBSplineData()
	>>> block.num_short_control_points = 50
	>>> block.short_control_points.update_size()
	>>> for i in range(block.num_short_control_points):
	...	 block.short_control_points[i] = 20 - i
	>>> list(block.get_short_data(12, 4, 3))
	[(8, 7, 6), (5, 4, 3), (2, 1, 0), (-1, -2, -3)]
	>>> offset = block.append_short_data([(1,2),(4,3),(13,14),(8,2),(33,33)])
	>>> offset
	50
	>>> list(block.get_short_data(offset, 5, 2))
	[(1, 2), (4, 3), (13, 14), (8, 2), (33, 33)]
	>>> list(block.get_comp_data(offset, 5, 2, 10.0, 32767.0))
	[(11.0, 12.0), (14.0, 13.0), (23.0, 24.0), (18.0, 12.0), (43.0, 43.0)]
	>>> block.append_float_data([(1.0,2.0),(3.0,4.0),(0.5,0.25)])
	0
	>>> list(block.get_float_data(0, 3, 2))
	[(1.0, 2.0), (3.0, 4.0), (0.5, 0.25)]
	>>> block.append_comp_data([(1,2),(4,3)])
	(60, 2.5, 1.5)
	>>> list(block.get_short_data(60, 2, 2))
	[(-32767, -10922), (32767, 10922)]
	>>> list(block.get_comp_data(60, 2, 2, 2.5, 1.5)) # doctest: +ELLIPSIS
	[(1.0, 2.00...), (4.0, 2.99...)]
	"""
	def _getData(self, offset, num_elements, element_size, controlpoints):
		"""Helper function for get_float_data and get_short_data. For internal
		use only."""
		# check arguments
		if not (controlpoints is self.float_control_points
				or controlpoints is self.short_control_points):
			raise ValueError("internal error while appending data")
		# parse the data
		for element in range(num_elements):
			yield tuple(
				controlpoints[offset + element * element_size + index]
				for index in range(element_size))

	def _appendData(self, data, controlpoints):
		"""Helper function for append_float_data and append_short_data. For internal
		use only."""
		# get number of elements
		num_elements = len(data)
		# empty list, do nothing
		if num_elements == 0:
			return
		# get element size
		element_size = len(data[0])
		# store offset at which we append the data
		if controlpoints is self.float_control_points:
			offset = self.num_float_control_points
			self.num_float_control_points += num_elements * element_size
		elif controlpoints is self.short_control_points:
			offset = self.num_short_control_points
			self.num_short_control_points += num_elements * element_size
		else:
			raise ValueError("internal error while appending data")
		flattened_data = itertools.chain.from_iterable(data)
		controlpoints.extend(flattened_data)
		# return the offset
		return offset

	def get_short_data(self, offset, num_elements, element_size):
		"""Get an iterator to the data.

		:param offset: The offset in the data where to start.
		:param num_elements: Number of elements to get.
		:param element_size: Size of a single element.
		:return: A list of C{num_elements} tuples of size C{element_size}.
		"""
		return self._getData(
			offset, num_elements, element_size, self.short_control_points)

	def get_comp_data(self, offset, num_elements, element_size, bias, multiplier):
		"""Get an interator to the data, converted to float with extra bias and
		multiplication factor. If C{x} is the short value, then the returned value
		is C{bias + x * multiplier / 32767.0}.

		:param offset: The offset in the data where to start.
		:param num_elements: Number of elements to get.
		:param element_size: Size of a single element.
		:param bias: Value bias.
		:param multiplier: Value multiplier.
		:return: A list of C{num_elements} tuples of size C{element_size}.
		"""
		for key in self.get_short_data(offset, num_elements, element_size):
			yield tuple(bias + x * multiplier / 32767.0 for x in key)

	def append_short_data(self, data):
		"""Append data.

		:param data: A list of elements, where each element is a tuple of
			integers. (Note: cannot be an interator; maybe this restriction
			will be removed in a future version.)
		:return: The offset at which the data was appended."""
		return self._appendData(data, self.short_control_points)

	def append_comp_data(self, data):
		"""Append data as compressed list.

		:param data: A list of elements, where each element is a tuple of
			integers. (Note: cannot be an interator; maybe this restriction
			will be removed in a future version.)
		:return: The offset, bias, and multiplier."""
		# get extremes
		maxvalue = max(max(datum) for datum in data)
		minvalue = min(min(datum) for datum in data)
		# get bias and multiplier
		bias = 0.5 * (maxvalue + minvalue)
		if maxvalue > minvalue:
			multiplier = 0.5 * (maxvalue - minvalue)
		else:
			# no need to compress in this case
			multiplier = 1.0

		# compress points into shorts
		shortdata = []
		for datum in data:
			shortdata.append(tuple(int(32767 * (x - bias) / multiplier)
								   for x in datum))
		return (self._appendData(shortdata, self.short_control_points),
				bias, multiplier)

	def get_float_data(self, offset, num_elements, element_size):
		"""Get an iterator to the data.

		:param offset: The offset in the data where to start.
		:param num_elements: Number of elements to get.
		:param element_size: Size of a single element.
		:return: A list of C{num_elements} tuples of size C{element_size}.
		"""
		return self._getData(
			offset, num_elements, element_size, self.float_control_points)

	def append_float_data(self, data):
		"""Append data.

		:param data: A list of elements, where each element is a tuple of
			floats. (Note: cannot be an interator; maybe this restriction
			will be removed in a future version.)
		:return: The offset at which the data was appended."""
		return self._appendData(data, self.float_control_points)
