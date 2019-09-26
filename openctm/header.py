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

    DEFAULTS = (b'OCTM', 5, b'RAW', 0, 0, 0, 0, 0)

    def __init__(self, header=None, **header_options):
        self.header = header or np.array([self.DEFAULTS], dtype=self.HEADER_TYPE)
        self.update_header_properties(**header_options)

    def __array__(self):
        return self.header

    @classmethod
    def load(cls, file_obj):
        header = np.copy(np.frombuffer(file_obj.read(cls.HEADER_TYPE.itemsize), dtype=cls.HEADER_TYPE))
        return cls(header)

    @property
    def header_property_names(self):
        return {name for name in self.HEADER_TYPE.names}

    @property
    def header_properties(self):
        return {name:value for name, value in zip(self.HEADER_TYPE.names, self.header[0])}

    def update_header_properties(self, **updates):
        updated_header_properties = {**self.header_properties, **updates}
        self.header[0] = tuple(str.encode(v) if isinstance(v, str) else v for v in updated_header_properties.values())

    def __getattr__(self, name):
        if name in self.header_property_names:
            return self.header_properties[name]
        else:
            raise AttributeError(f"{self} has no attribute {name}")

    def __setattr__(self, name, value):
        if name in self.header_property_names:
            self.update_header_properties(**{name:value})
        else:
            super().__setattr__(name, value)

