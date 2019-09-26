import numpy as np

from . import utils

NORMALS=0x00000001

class RAW:

    @staticmethod
    def decode_body(f, header):

        # Faces
        assert utils.read_string(f, 4) == 'INDX'
        faces = utils.read_int_32_array(f, 3 * header.face_count).reshape(-1, 3)

        # Vertices
        assert utils.read_string(f, 4) == 'VERT'
        vertices = utils.read_float_32_array(f, 3 * header.vertex_count).reshape(-1, 3)

        # Normals
        face_normals = None
        if header.flags & NORMALS:
            assert utils.read_string(f, 4) == 'NORM'
            face_normals = utils.read_float_32_array(f, 3 * header.vertex_count).reshape(-1, 3)

        return vertices, faces, face_normals

    @staticmethod
    def encode_body(f, mesh_dict, header):

        # Faces
        utils.write_string(f, 'INDX')
        utils.write_int_32_array(f, mesh_dict['faces'].reshape(-1))

        # Vertices
        utils.write_string(f, 'VERT')
        utils.write_float_32_array(f, mesh_dict['vertices'].reshape(-1))

        # Normals
        if (header.flags & NORMALS) and mesh_dict['face_normals'] is not None:
            utils.write_string(f, 'NORM')
            utils.write_float_32_array(f, mesh_dict['face_normals'].reshape(-1))

class MG1(RAW):

    @staticmethod
    def decode_body(f, header):

        # Indices
        assert utils.read_string(f, 4) == 'INDX'
        faces = utils.read_packed_data(f, header.face_count, np.dtype('<i'), stride=3)
        faces = utils.delta_decode(faces).reshape(-1, 3)

        # Vertices
        assert utils.read_string(f, 4) == 'VERT'
        vertices = utils.read_packed_data(f, header.vertex_count, np.dtype('<f'), stride=1).reshape(-1, 3)

        # Normals
        face_normals = None
        if header.flags & NORMALS:
            assert utils.read_string(f, 4) == 'NORM'
            face_normals = utils.read_packed_data(f, header.vertex_count, np.dtype('<f'), stride=3).reshape(-1, 3)

        return vertices, faces, face_normals

    @staticmethod
    def encode_body(f, mesh_dict, header):

        # Indices
        utils.write_string(f, 'INDX')
        #faces = utils.delta_encode(mesh.faces.reshape(-1))
        #utils.write_packed_data(f, faces, stride=3)


class MG2(RAW):

    @staticmethod
    def decode_body(f, header):
        raise NotImplementedError("Not yet implemented")
