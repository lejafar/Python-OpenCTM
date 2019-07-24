"""
Copyright (c) 2018 Rafael Hautekiet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
References:
- "OpenCTM: The Open Compressed Triangle Mesh file format" by Marcus Geelnard
  http://openctm.sourceforge.net/
"""

NORMALS=0x00000001

import numpy as np
from types import SimpleNamespace
from collections import namedtuple

from . import utils

class CTM:

    HEADER_TYPE = np.dtype([('magic_identifier', np.dtype('S4')),
                             ('file_format', np.dtype('<i4')),
                             ('compression_method', np.dtype('S4')),
                             ('vertex_count', np.dtype('<i4')),
                             ('face_count', np.dtype('<i4')),
                             ('uv_map_count', np.dtype('<i4')),
                             ('attr_map_count', np.dtype('<i4')),
                             ('flags', np.dtype('<i4'))])

    def __init__(self, file_obj, opened, header, comment=""):
        self.file_obj = file_obj
        self.opened = opened
        self.header = header
        self.comment = comment

        self._body, self._custom_attributes = None, None

    @classmethod
    def compression_class(cls, method):
        """ in order to allow subclassing `CTM`, we create the inheritance dynamically """
        return {b'MG1': type('CTM_MG1_', (CTM_MG1, cls), {}),
                b'MG2': type('CTM_MG2_', (CTM_MG1, cls), {})}.get(method, CTM)

    @classmethod
    def load(cls, file_obj, **kwargs):

        try:
            # try reading header
            opened = False
            header, comment = cls.read_header(file_obj)
        except AttributeError as e:
            file_obj = open(file_obj, 'rb')
            opened = True # we'll also have to close it
            header, comment = cls.read_header(file_obj)

        return cls.compression_class(header.compression_method)(file_obj, opened, header, comment, **kwargs)

    @classmethod
    def read_header(cls, f, **kwargs):
        header = np.frombuffer(f.read(cls.HEADER_TYPE.itemsize), dtype=cls.HEADER_TYPE)
        header = SimpleNamespace(**{k: header[k][0] for k in header.dtype.names})
        comment = utils.read_string(f)
        header.header_size = f.tell()
        return header, comment

    @property
    def faces(self):
        return self.body.indices

    @property
    def vertices(self):
        return self.body.vertices

    @property
    def normals(self):
        return self.body.normals

    @property
    def body(self):

        if self._body is not None:
            return self._body

        body = SimpleNamespace(indices=None, vertices=None, normals=None)
        self._body = self.read_body(body, self.file_obj)
        return self._body


    def read_body(self, body, f):
        raise NotImplementedError("not yet implemented")


    def __del__(self):
        if self.opened:
            # we only want to close the file_obj
            # if we are the ones that opened it
            self.file_obj.close()

    def __repr__(self):
        return f"{self.__class__.__name__}<n_vertices={self.header.vertex_count}, n_faces={self.header.face_count}>"

class CTM_MG1:

    def read_body(self, body, f):

        # Indices
        assert utils.read_string(f, 4) == 'INDX'
        body.indices = utils.read_packed_data(self.file_obj, self.header.face_count, np.dtype('<i'), stride=3)
        body.indices = utils.delta_decode(body.indices).reshape(-1, 3)

        # Vertices
        assert utils.read_string(f, 4) == 'VERT'
        body.vertices = utils.read_packed_data(f, self.header.vertex_count, np.dtype('<f'), stride=1).reshape(-1, 3)

        # Normals
        if self.header.flags & NORMALS:
            assert utils.read_string(f, 4) == 'NORM'
            body.normals = utils.read_packed_data(f, self.header.vertex_count, np.dtype('<f'), stride=3).reshape(-1, 3)

        return body

class CTM_MG2:

    def read_body(self, body, f):
        raise NotImplementedError("Not yet implemented")


