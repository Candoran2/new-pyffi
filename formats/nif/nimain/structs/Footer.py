# START_GLOBALS
import struct

# END_GLOBALS

class Footer:
# START_CLASS

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = super().from_stream(stream, context, arg, template)
		modification = getattr(context, "modification", None)
		if modification == "neosteam":
			extrabyte, = struct.unpack("<B", stream.read(1))
			if extrabyte != 0:
				raise ValueError(f"Expected trailing zero byte in footer, but got {extrabyte} instead.")
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		super().to_stream(stream, instance)
		modification = getattr(instance.context, "modification", None)
		if modification == "neosteam":
			stream.write("\x00".encode("ascii"))
		return instance