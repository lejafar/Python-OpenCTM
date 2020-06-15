import numpy as np

from . import utils
from .compression import MG1, MG2, RAW
from .header import CTMHeader

class CTMReader:

    """ singleton class responsible for writing ctm body """

    def __new__(cls, file_obj):
        try:
            # try to read it
            return cls.read(file_obj)
        except AttributeError as e:
            # try to open it first
            with open(file_obj, 'rb') as file_obj:
                return cls.read(file_obj)

    @classmethod
    def read(cls, file_obj):
        # read ctm file
        header = cls.read_header(file_obj)
        comment = utils.read_string(file_obj) # TODO: test this more
        body = cls.read_body(file_obj, header)
        return body, header

    @classmethod
    def read_header(cls, file_obj):
        """ read header """
        return CTMHeader.load(file_obj)

    @classmethod
    def read_body(cls, file_obj, header):
        """ read body """

        transcoder = {b'MG1': MG1,
                      b'MG2': MG2}.get(header.compression_method, RAW)

        vertices, faces, face_normals = transcoder.decode_body(file_obj, header)
        return {"vertices": vertices, "faces": faces, "face_normals": face_normals}

