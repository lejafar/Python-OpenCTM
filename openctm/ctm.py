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
from .reader import CTMReader, CTMHeader
from .writer import CTMWriter

import numpy as np


class CTM:

    READER = CTMReader
    WRITER = CTMWriter
    DEFAULT_COMPRESSION = 'RAW'

    def __init__(self, vertices, faces, face_normals=None, header=None):
        self._mesh_dict = {}
        self._header = header

        self.vertices = vertices
        self.faces = faces
        self.face_normals = face_normals

    @property
    def vertices(self):
        return self._mesh_dict.get('vertices')

    @vertices.setter
    def vertices(self, value):
        self._mesh_dict['vertices'] = value

    @property
    def faces(self):
        return self._mesh_dict.get('faces')

    @faces.setter
    def faces(self, value):
        self._mesh_dict['faces'] = value

    @property
    def face_normals(self):
        return self._mesh_dict.get('face_normals')

    @face_normals.setter
    def face_normals(self, value):
        self._mesh_dict['face_normals'] = value

    @property
    def header(self):
        if not self._header:
            self._header = CTMHeader(compression_method=self.DEFAULT_COMPRESSION)

        # enforce the header to be always consistent with the content
        self._header.vertex_count = len(self.vertices)
        self._header.face_count = len(self.faces)

        return self._header

    @classmethod
    def load(cls, file_obj):
        mesh_dict, header = cls.READER(file_obj)
        return cls(**mesh_dict, header=header)

    def export(self, file_obj):
        # enforce RAW temporarily
        header = self.header
        header.compression_method = 'RAW'
        self.WRITER(file_obj, self._mesh_dict, header)

    def __repr__(self):
        return f"{self.__class__.__name__}<n_vertices={self.header.vertex_count}, n_faces={self.header.face_count}>"





