import numpy as np

from . import utils

class CTMHeader:

    HEADER_TYPE = np.dtype([('magic_identifier', np.dtype('S4')),
        ('file_format', np.dtype('<i4')),
        ('compression_method', np.dtype('S4')),
        ('vertex_count', np.dtype('<i4')),
        ('face_count', np.dtype('<i4')),
        ('uv_map_count', np.dtype('<i4')),
        ('attr_map_count', np.dtype('<i4')),
        ('flags', np.dtype('<i4'))])

    def __init__(self, header=None, comment=None, header_size=None):
        self.header = header
        self.comment = comment
        self.header_size = header_size

    def __array__(self):
        return self.header

    @classmethod
    def load(cls, file_obj):
        header = np.frombuffer(file_obj.read(cls.HEADER_TYPE.itemsize), dtype=cls.HEADER_TYPE)
        comment = utils.read_string(file_obj) # TODO: test this more
        header_size = file_obj.tell()
        return cls(header, comment, header_size)

    @property
    def header_properties(self):
        return {k:v for k, v in zip(self.header.dtype.names, self.header[0])}

    def __getattr__(self, name):
        if name in self.header_properties:
            return self.header_properties[name]
        else:
            raise AttributeError(f"{self} has no attribute {name}")
