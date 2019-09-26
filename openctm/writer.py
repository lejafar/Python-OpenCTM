import numpy as np

from . import utils
from . import compression
from .header import CTMHeader

class CTMWriter:

    """ singleton class responsible for writing """

    @classmethod
    def make_header(cls, mesh_dict):
        """ make header when none is available """
        header = CTMHeader()
        header.vertex_count = len(mesh_dict['vertices'])
        header.face_count = len(mesh_dict['faces'])
        # TODO: set normals flag
        return header

    def __new__(cls, file_obj, mesh_dict, header=None, **header_options):
        if header is None:
            header = cls.make_header(mesh_dict)
            header.update_header_properties(**header_options)
        try:
            # try to write to it
            return cls.write(file_obj, mesh_dict, header)
        except AttributeError as e:
            # try to open it first
            with open(file_obj, 'wb') as file_obj:
                return cls.write(file_obj, mesh_dict, header)

    @classmethod
    def write(cls, file_obj, mesh_dict, header):
        # write ctm file
        cls.write_header(file_obj, header)
        cls.write_body(file_obj, mesh_dict, header)

    @classmethod
    def write_header(cls, file_obj, header):
        header = np.asanyarray(header)
        file_obj.write(header.tobytes())
        utils.write_int_32(file_obj, 0) # no comment

    @classmethod
    def write_body(cls, file_obj, mesh_dict, header):

        transcoder = {b'MG1': compression.MG1,
                      b'MG2': compression.MG2}.get(header.compression_method, compression.RAW)

        compression.RAW.encode_body(file_obj, mesh_dict, header)
