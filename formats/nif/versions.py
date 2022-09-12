def version_from_str(version_str):
	"""Converts version string into an integer.

	:param version_str: The version string.
	:type version_str: str
	:return: A version integer.

	>>> hex(NifFormat.version_number('3.14.15.29'))
	'0x30e0f1d'
	>>> hex(NifFormat.version_number('1.2'))
	'0x1020000'
	>>> hex(NifFormat.version_number('3.03'))
	'0x3000300'
	>>> hex(NifFormat.version_number('NS'))
	'0xa010000'
	"""

	# 3.03 case is special
	if version_str == '3.03':
		return 0x03000300

	# NS (neosteam) case is special
	if version_str == 'NS':
		return 0x0A010000

	try:
		ver_list = [int(x) for x in version_str.split('.')]
	except ValueError:
		return -1 # version not supported (i.e. version_str '10.0.1.3a' would trigger this)
	if len(ver_list) > 4 or len(ver_list) < 1:
		return -1 # version not supported
	for ver_digit in ver_list:
		if (ver_digit | 0xff) > 0xff:
			return -1 # version not supported
	while len(ver_list) < 4: ver_list.append(0)
	return (ver_list[0] << 24) + (ver_list[1] << 16) + (ver_list[2] << 8) + ver_list[3]


