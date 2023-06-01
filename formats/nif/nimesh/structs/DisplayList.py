import numpy as np
from struct import Struct

from generated.utils.tristrip import triangulate


ushort_struct = Struct('>H')

def unknown_command_function(data_len):
    def command_function(displaylist, index):
        index += 1
        return displaylist.bytes_array[index:index + data_len], index + data_len
    return command_function

def nop(displaylist, index):
    return [], index + 1

def triangles(displaylist, index):
    index += 1
    data_start = index
    bytes_array = displaylist.bytes_array
    num_vertices = ushort_struct.unpack(bytes_array[index:index + 2].tobytes())[0]
    index += 2
    index += num_vertices * displaylist.vert_struct.size * (4 + (1 if displaylist.has_weights else 0))
    return bytes_array[data_start:index], index

def triangle_strip(displaylist, index):
    return triangles(displaylist, index)


class DisplayList:
    """This code is based on the information in https://wiki.tockdom.com/wiki/Wii_Graphics_Code"""
    
    # command_map maps command bytes to functions which take in the array and the current position and return an object
    # and the next position
    command_map = {0x00: nop,
                   0x20: unknown_command_function(2),
                   0x28: unknown_command_function(2),
                   0x84: unknown_command_function(1),
                   0xb0: unknown_command_function(1),
                   0x90: triangles,
                   0x98: triangle_strip}

    def __init__(self, bytes_list):
        """Create a display list object from the bytes_array iterator (must contain integers between 0 and 255)"""
        self.bytes_array = np.array(bytes_list, dtype=np.uint8)
        self.vert_struct = None
        self.has_weights = False
        self.commands = []
        self.values = []

    def read_commands(self):
        index = 0
        bytes_array = self.bytes_array
        arr_len = len(bytes_array)
        commands = []
        values = []
        while index < arr_len:
            command = bytes_array[index]
            commands.append(command)
            value, index = self.command_map[command](self, index)
            values.append(value)
        self.commands = commands
        self.values = values

    def create_mesh_data(self, owning_nimesh):
		# strategy:
		# 1. Get mesh information (position, normal, color and UV coordinates, as well as weight information if relevant)
		# 2. determine uint lengths (byte vs ushort, maybe vs uint?) depending on the longest mesh information array
		# 3. Read the commands. Depending
        self.has_weights = owning_nimesh.extra_em_data.has_weights
        positions = []
        positions.extend(owning_nimesh.geomdata_by_name("POSITION", False, False))
        positions.extend(owning_nimesh.geomdata_by_name("POSITION_BP", False, False))
        normals = []
        normals.extend(owning_nimesh.geomdata_by_name("NORMAL", False, False))
        normals.extend(owning_nimesh.geomdata_by_name("NORMAL_BP", False, False))
        colors = owning_nimesh.geomdata_by_name("COLOR", False, False)
        UVs = owning_nimesh.geomdata_by_name("TEXCOORD", False, False)
        vertex_datas = [positions, normals, colors, UVs]

        max_len = max(len(data) for data in vertex_datas)
        if max_len < 256:
            self.vert_struct = Struct('>B')
        elif max_len < 65536:
            self.vert_struct = Struct('>H')
        else:
            self.vert_struct = Struct('>I')
        vert_length = self.vert_struct.size * 4
        base_info_start = 0
        if self.has_weights:
            vert_length += self.vert_struct.size
            base_info_start = 1

        self.read_commands()

        total_vertex_datas = [[] for data in vertex_datas]
        triangles = []
        total_vertices_map = {}
        for command, parameters in zip(self.commands, self.values):
            if command in (0x90, 0x98):

                vertex_indices = []
                for vert_index in range(2, len(parameters), vert_length):
                    vert_bytes = parameters[vert_index:vert_index + vert_length]
                    vert_integers = [self.vert_struct.unpack(b_int.tobytes())[0] for b_int in vert_bytes.reshape((-1, self.vert_struct.size))]
                    vert_integers = tuple(vert_integers[base_info_start:])
                    if vert_integers not in total_vertices_map:
                        total_vertices_map[vert_integers] = len(total_vertices_map)
                        for i in range(4):
                            total_vertex_datas[i].append(vertex_datas[i][vert_integers[i]])
                    vertex_indices.append(total_vertices_map[vert_integers])
                if command == 0x90:
                    triangles.extend([vertex_indices[i:i + 3] for i in range(0, len(vertex_indices) - 2, 3)])
                else:
                    triangles.extend(triangulate([vertex_indices]))

        return total_vertex_datas, triangles