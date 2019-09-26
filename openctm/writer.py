import numpy as np

from . import utils
from . import compression

class CTMWriter:

    def __new__(cls, file_obj, mesh_dict, header):
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

        transcoder.encode_body(file_obj, mesh_dict, header)
