# START_GLOBALS
import generated.formats.nif as NifFormat
# END_GLOBALS

class NiPixelFormat:
# START_CLASS
	def save_as_dds(self, stream):
		"""Save image as DDS file."""
		# set up header and pixel data
		data = pyffi.formats.dds.DdsFormat.Data()
		header = data.header
		pixeldata = data.pixeldata

		# create header, depending on the format
		if self.pixel_format in (NifFormat.classes.PixelFormat.PX_FMT_RGB8,
								 NifFormat.classes.PixelFormat.PX_FMT_RGBA8):
			# uncompressed RGB(A)
			header.flags.caps = 1
			header.flags.height = 1
			header.flags.width = 1
			header.flags.pixel_format = 1
			header.flags.mipmap_count = 1
			header.flags.linear_size = 1
			header.height = self.mipmaps[0].height
			header.width = self.mipmaps[0].width
			header.linear_size = len(self.pixel_data)
			header.mipmap_count = len(self.mipmaps)
			header.pixel_format.flags.rgb = 1
			header.pixel_format.bit_count = self.bits_per_pixel
			if not self.channels:
				header.pixel_format.r_mask = self.red_mask
				header.pixel_format.g_mask = self.green_mask
				header.pixel_format.b_mask = self.blue_mask
				header.pixel_format.a_mask = self.alpha_mask
			else:
				bit_pos = 0
				for i, channel in enumerate(self.channels):
					mask = (2 ** channel.bits_per_channel - 1) << bit_pos
					if channel.type == NifFormat.classes.ChannelType.CHNL_RED:
						header.pixel_format.r_mask = mask
					elif channel.type == NifFormat.classes.ChannelType.CHNL_GREEN:
						header.pixel_format.g_mask = mask
					elif channel.type == NifFormat.classes.ChannelType.CHNL_BLUE:
						header.pixel_format.b_mask = mask
					elif channel.type == NifFormat.classes.ChannelType.CHNL_ALPHA:
						header.pixel_format.a_mask = mask
					bit_pos += channel.bits_per_channel
			header.caps_1.complex = 1
			header.caps_1.texture = 1
			header.caps_1.mipmap = 1
			if self.pixel_data:
				# used in older nif versions
				pixeldata.set_value(self.pixel_data)
			else:
				# used in newer nif versions
				pixeldata.set_value(''.join(self.pixel_data_matrix))
		elif self.pixel_format == NifFormat.classes.PixelFormat.PX_FMT_DXT1:
			# format used in Megami Tensei: Imagine and Bully SE
			header.flags.caps = 1
			header.flags.height = 1
			header.flags.width = 1
			header.flags.pixel_format = 1
			header.flags.mipmap_count = 1
			header.flags.linear_size = 0
			header.height = self.mipmaps[0].height
			header.width = self.mipmaps[0].width
			header.linear_size = 0
			header.mipmap_count = len(self.mipmaps)
			header.pixel_format.flags.four_c_c = 1
			header.pixel_format.four_c_c = pyffi.formats.dds.DdsFormat.FourCC.DXT1
			header.pixel_format.bit_count = 0
			header.pixel_format.r_mask = 0
			header.pixel_format.g_mask = 0
			header.pixel_format.b_mask = 0
			header.pixel_format.a_mask = 0
			header.caps_1.complex = 1
			header.caps_1.texture = 1
			header.caps_1.mipmap = 1
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
			header.flags.caps = 1
			header.flags.height = 1
			header.flags.width = 1
			header.flags.pixel_format = 1
			header.flags.mipmap_count = 1
			header.flags.linear_size = 0
			header.height = self.mipmaps[0].height
			header.width = self.mipmaps[0].width
			header.linear_size = 0
			header.mipmap_count = len(self.mipmaps)
			header.pixel_format.flags.four_c_c = 1
			header.pixel_format.four_c_c = pyffi.formats.dds.DdsFormat.FourCC.DXT5
			header.pixel_format.bit_count = 0
			header.pixel_format.r_mask = 0
			header.pixel_format.g_mask = 0
			header.pixel_format.b_mask = 0
			header.pixel_format.a_mask = 0
			header.caps_1.complex = 1
			header.caps_1.texture = 1
			header.caps_1.mipmap = 1
			pixeldata.set_value(''.join(self.pixel_data_matrix))
		else:
			raise ValueError(
				"cannot save pixel format %i as DDS" % self.pixel_format)

		data.write(stream)
