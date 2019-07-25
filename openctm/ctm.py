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

    def __init__(self, file_obj):
        self.file_obj = file_obj
        self.opened = False

        self._header = None
        self._body = None
        self.comment = None

    @property
    def reader(self):
        return {b'MG1': MG1,
                b'MG2': MG2}.get(self.header.compression_method, RAW)

    @property
    def header(self):

        if self._header is not None:
            return self._header

        try:
            # try reading header
            self._header, self.comment = self.read_header(self.file_obj)
        except AttributeError as e:
            self.file_obj = open(self.file_obj, 'rb')
            self.opened = True # we'll also have to close it
            self._header, self.comment = self.read_header(self.file_obj)

        return self._header

    def read_header(self, f, **kwargs):
        header = np.frombuffer(f.read(self.HEADER_TYPE.itemsize), dtype=self.HEADER_TYPE)
        header = SimpleNamespace(**{k: header[k][0] for k in header.dtype.names})
        comment = utils.read_string(f)
        header.header_size = f.tell()
        return header, comment

    @property
    def body(self):

        if self._body is not None:
            return self._body

        body = SimpleNamespace(indices=None, vertices=None, normals=None)
        self._body = self.reader.read_body(body, self.header, self.file_obj)
        return self._body

    @property
    def faces(self):
        return self.body.indices

    @property
    def vertices(self):
        return self.body.vertices

    @property
    def normals(self):
        return self.body.normals

    def __del__(self):
        if self.opened:
            # we only want to close the file_obj
            # if we are the ones that opened it
            self.file_obj.close()

    def __repr__(self):
        return f"{self.__class__.__name__}<n_vertices={self.header.vertex_count}, n_faces={self.header.face_count}>"

class RAW:

    @staticmethod
    def read_body(body, header, f):
        raise NotImplementedError("Not yet implemented")

class MG1(RAW):

    @staticmethod
    def read_body(body, header, f):

        # Indices
        assert utils.read_string(f, 4) == 'INDX'
        body.indices = utils.read_packed_data(f, header.face_count, np.dtype('<i'), stride=3)
        body.indices = utils.delta_decode(body.indices).reshape(-1, 3)

        # Vertices
        assert utils.read_string(f, 4) == 'VERT'
        body.vertices = utils.read_packed_data(f, header.vertex_count, np.dtype('<f'), stride=1).reshape(-1, 3)

        # Normals
        if header.flags & NORMALS:
            assert utils.read_string(f, 4) == 'NORM'
            body.normals = utils.read_packed_data(f, header.vertex_count, np.dtype('<f'), stride=3).reshape(-1, 3)

        return body

class MG2(RAW):

    @staticmethod
    def read_body(body, header, f):
        raise NotImplementedError("Not yet implemented")


