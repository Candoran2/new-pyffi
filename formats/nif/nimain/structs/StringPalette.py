# START_GLOBALS
import logging

import generated.formats.nif as NifFormat

_b00 = b"\x00"
# END_GLOBALS

class StringPalette:

# START_CLASS
	def get_string(self, offset):
		"""Return string at given offset.

		>>> from pyffi.formats.nif import NifFormat
		>>> pal = NifFormat.StringPalette()
		>>> pal.add_string("abc")
		0
		>>> pal.add_string("def")
		4
		>>> print(pal.get_string(0).decode("ascii"))
		abc
		>>> print(pal.get_string(4).decode("ascii"))
		def
		>>> pal.get_string(5) # doctest: +ELLIPSIS
		pyffi.nif.stringpalette:WARNING:StringPalette: no string starts at offset 5 (string is b'ef', preceeding character is b'd')
		b'ef'
		>>> pal.get_string(100) # doctest: +ELLIPSIS
		Traceback (most recent call last):
			...
		ValueError: ...
		"""
		palette_bytes = NifFormat.encode(self.palette)
		# check that offset isn't too large
		if offset >= len(palette_bytes):
			raise ValueError(
				f"StringPalette: getting string at {offset} "
				f"but palette is only {len(palette_bytes)} long")
		# check that a string starts at this offset
		if offset > 0 and palette_bytes[offset-1:offset] != _b00:
			logger = logging.getLogger("generated.nif.stringpalette")
			logger.warning(
				f"StringPalette: no string starts at offset {offset} "
				f"(string is {palette_bytes[offset:palette_bytes.find(_b00, offset)]}, "
				f"preceeding character is {self.palette[offset-1:offset]})")
		# return the string
		return NifFormat.safe_decode(palette_bytes[offset:palette_bytes.find(_b00, offset)])

	def get_all_strings(self):
		"""Return a list of all strings.

		>>> from pyffi.formats.nif import NifFormat
		>>> pal = NifFormat.StringPalette()
		>>> pal.add_string("abc")
		0
		>>> pal.add_string("def")
		4
		>>> for x in pal.get_all_strings():
		...	 print(x.decode("ascii"))
		abc
		def
		>>> # pal.palette.decode("ascii") needs lstrip magic for py3k
		>>> print(repr(pal.palette.decode("ascii")).lstrip("u"))
		'abc\\x00def\\x00'
		"""
		return [NifFormat.safe_decode(entry) for entry in self.palette[:-1].split(str(_b00))]

	def add_string(self, text):
		"""Adds string to palette (will recycle existing strings if possible) and
		return offset to the string in the palette.

		>>> from pyffi.formats.nif import NifFormat
		>>> pal = NifFormat.StringPalette()
		>>> pal.add_string("abc")
		0
		>>> pal.add_string("abc")
		0
		>>> pal.add_string("def")
		4
		>>> pal.add_string("")
		-1
		>>> print(pal.get_string(4).decode("ascii"))
		def
		"""
		palette_bytes = NifFormat.encode(self.palette)
		# empty text
		if not text:
			return -1
		# convert text to bytes if necessary
		if isinstance(text, str):
			text = NifFormat.encode(text)
		# check if string is already in the palette
		# ... at the start
		if text + _b00 == palette_bytes[:len(text) + 1]:
			return 0
		# ... or elsewhere
		offset = palette_bytes.find(_b00 + text + _b00)
		if offset != -1:
			return offset + 1
		# if no match, add the string
		if offset == -1:
			offset = len(palette_bytes)
			palette_bytes = palette_bytes + text + _b00
			self.palette = NifFormat.safe_decode(palette_bytes)
			self.length = len(palette_bytes)
		# return the offset
		return offset

	def clear(self):
		"""Clear all strings in the palette.

		>>> from pyffi.formats.nif import NifFormat
		>>> pal = NifFormat.StringPalette()
		>>> pal.add_string("abc")
		0
		>>> pal.add_string("def")
		4
		>>> # pal.palette.decode("ascii") needs lstrip magic for py3k
		>>> print(repr(pal.palette.decode("ascii")).lstrip("u"))
		'abc\\x00def\\x00'
		>>> pal.clear()
		>>> # pal.palette.decode("ascii") needs lstrip magic for py3k
		>>> print(repr(pal.palette.decode("ascii")).lstrip("u"))
		''
		"""
		self.palette = "" # empty string object
		self.length = 0
