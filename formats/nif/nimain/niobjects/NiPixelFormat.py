# START_GLOBALS
import generated.formats.nif as NifFormat
from generated.formats.dds import DdsFile
from generated.formats.dds.enums.FourCC import FourCC
# END_GLOBALS

class NiPixelFormat:
# START_CLASS

	def _get_pixeldata_stream(self):
		return bytes(self.pixel_data)

	def save_as_dds(self, stream):
		"""Save image as DDS file."""
		# set up header and pixel data
		file = DdsFile()

		# create header, depending on the format
		if self.pixel_format in (NifFormat.classes.PixelFormat.FMT_RGB,
								 NifFormat.classes.PixelFormat.FMT_RGBA):
			# uncompressed RGB(A)
			file.flags.caps = 1
			file.flags.height = 1
			file.flags.width = 1
			file.flags.pixel_format = 1
			file.flags.mipmap_count = 1
			file.flags.linear_size = 1
			file.height = self.mipmaps[0].height
			file.width = self.mipmaps[0].width
			file.linear_size = len(self.pixel_data) // self.num_pixels # we want it to be 1 for version <= 10.2.0.0?
			file.mipmap_count = len(self.mipmaps)
			file.pixel_format.flags.four_c_c = 0
			file.pixel_format.flags.rgb = 1
			file.pixel_format.four_c_c = FourCC.LINEAR
			file.pixel_format.bit_count = self.bits_per_pixel
			if not self.channels:
				file.pixel_format.r_mask = self.red_mask
				file.pixel_format.g_mask = self.green_mask
				file.pixel_format.b_mask = self.blue_mask
				file.pixel_format.a_mask = self.alpha_mask
			else:
				bit_pos = 0
				for i, channel in enumerate(self.channels):
					mask = (2 ** channel.bits_per_channel - 1) << bit_pos
					if channel.type == NifFormat.classes.PixelComponent.COMP_RED:
						file.pixel_format.r_mask = mask
					elif channel.type == NifFormat.classes.PixelComponent.COMP_GREEN:
						file.pixel_format.g_mask = mask
					elif channel.type == NifFormat.classes.PixelComponent.COMP_BLUE:
						file.pixel_format.b_mask = mask
					elif channel.type == NifFormat.classes.PixelComponent.COMP_ALPHA:
						file.pixel_format.a_mask = mask
					bit_pos += channel.bits_per_channel
			file.caps_1.complex = 1
			file.caps_1.texture = 1
			file.caps_1.mipmap = 1
			file.buffer = self._get_pixeldata_stream()
		elif self.pixel_format == NifFormat.classes.PixelFormat.FMT_DXT1:
			# format used in Megami Tensei: Imagine and Bully SE
			file.flags.caps = 1
			file.flags.height = 1
			file.flags.width = 1
			file.flags.pixel_format = 1
			file.flags.mipmap_count = 1
			file.flags.linear_size = 0
			file.height = self.mipmaps[0].height
			file.width = self.mipmaps[0].width
			file.linear_size = 0
			file.mipmap_count = len(self.mipmaps)
			file.pixel_format.flags.four_c_c = 1
			file.pixel_format.four_c_c = FourCC.DXT1
			file.pixel_format.bit_count = 0
			file.pixel_format.r_mask = 0
			file.pixel_format.g_mask = 0
			file.pixel_format.b_mask = 0
			file.pixel_format.a_mask = 0
			file.caps_1.complex = 1
			file.caps_1.texture = 1
			file.caps_1.mipmap = 1
			file.buffer = self._get_pixeldata_stream()
		elif self.pixel_format in (NifFormat.classes.PixelFormat.FMT_DXT3,
								   NifFormat.classes.PixelFormat.FMT_DXT5):
			# format used in Megami Tensei: Imagine
			file.flags.caps = 1
			file.flags.height = 1
			file.flags.width = 1
			file.flags.pixel_format = 1
			file.flags.mipmap_count = 1
			file.flags.linear_size = 0
			file.height = self.mipmaps[0].height
			file.width = self.mipmaps[0].width
			file.linear_size = 0
			file.mipmap_count = len(self.mipmaps)
			file.pixel_format.flags.four_c_c = 1
			file.pixel_format.four_c_c = FourCC.DXT5
			file.pixel_format.bit_count = 0
			file.pixel_format.r_mask = 0
			file.pixel_format.g_mask = 0
			file.pixel_format.b_mask = 0
			file.pixel_format.a_mask = 0
			file.caps_1.complex = 1
			file.caps_1.texture = 1
			file.caps_1.mipmap = 1
			file.buffer = self._get_pixeldata_stream()
		else:
			raise ValueError(
				"cannot save pixel format %i as DDS" % self.pixel_format)

		file.write(stream)
