import numpy as np

from . import utils
from .compression import MG1, MG2, RAW
from .header import CTMHeader

class CTMReader:

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
        header = cls.header(file_obj)
        vertices, faces, face_normals = cls.body(file_obj, header)
        return {"vertices": vertices,
                "faces": faces,
                "face_normals": face_normals}, header

    @classmethod
    def header(cls, file_obj, **kwargs):
        """ read header """
        return CTMHeader.load(file_obj)

    @classmethod
    def body(cls, file_obj, header):
        """ read body """

        transcoder = {b'MG1': MG1,
                      b'MG2': MG2}.get(header.compression_method, RAW)

        return transcoder.decode_body(file_obj, header)
