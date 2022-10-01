# START_GLOBALS
import generated.formats.nif as NifFormat
from generated.formats.dds import DdsFile
# END_GLOBALS

class NiPixelFormat:
# START_CLASS
	def save_as_dds(self, stream):
		"""Save image as DDS file."""
		# set up header and pixel data
		file = DdsFile()
		pixeldata = file.pixeldata

		# create header, depending on the format
		if self.pixel_format in (NifFormat.classes.PixelFormat.PX_FMT_RGB8,
								 NifFormat.classes.PixelFormat.PX_FMT_RGBA8):
			# uncompressed RGB(A)
			file.flags.caps = 1
			file.flags.height = 1
			file.flags.width = 1
			file.flags.pixel_format = 1
			file.flags.mipmap_count = 1
			file.flags.linear_size = 1
			file.height = self.mipmaps[0].height
			file.width = self.mipmaps[0].width
			file.linear_size = len(self.pixel_data)
			file.mipmap_count = len(self.mipmaps)
			file.pixel_format.flags.rgb = 1
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
					if channel.type == NifFormat.classes.ChannelType.CHNL_RED:
						file.pixel_format.r_mask = mask
					elif channel.type == NifFormat.classes.ChannelType.CHNL_GREEN:
						file.pixel_format.g_mask = mask
					elif channel.type == NifFormat.classes.ChannelType.CHNL_BLUE:
						file.pixel_format.b_mask = mask
					elif channel.type == NifFormat.classes.ChannelType.CHNL_ALPHA:
						file.pixel_format.a_mask = mask
					bit_pos += channel.bits_per_channel
			file.caps_1.complex = 1
			file.caps_1.texture = 1
			file.caps_1.mipmap = 1
			if self.pixel_data:
				# used in older nif versions
				pixeldata.set_value(self.pixel_data)
			else:
				# used in newer nif versions
				pixeldata.set_value(''.join(self.pixel_data_matrix))
		elif self.pixel_format == NifFormat.classes.PixelFormat.PX_FMT_DXT1:
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
			if isinstance(self,
						  NifFormat.classes.NiPersistentSrcTextureRendererData):
				pixeldata.set_value(
					''.join(
						''.join([chr(x) for x in tex])
						for tex in self.pixel_data))
			else:
				pixeldata.set_value(''.join(self.pixel_data_matrix))
		elif self.pixel_format in (NifFormat.classes.PixelFormat.PX_FMT_DXT5,
								   NifFormat.classes.PixelFormat.PX_FMT_DXT5_ALT):
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
			pixeldata.set_value(''.join(self.pixel_data_matrix))
		else:
			raise ValueError(
				"cannot save pixel format %i as DDS" % self.pixel_format)

		file.write(stream)
