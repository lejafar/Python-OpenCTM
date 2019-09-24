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
    DEFAULT_COMPRESSION = 'MG1'

    def __init__(self, vertices, faces, face_normals=None, header=None):
        self.vertices = vertices
        self.faces = faces
        self.face_normals = face_normals

        self._header = header

    @property
    def comment(self):
        return self.header.comment

    @property
    def header(self):
        if not self._header:
            self._header = CTMHeader(compression_method=self.DEFAULT_COMPRESSION)
        return self._header

    @property
    def mesh(self):
        return {"vertices": self.vertices,
                "faces": self.faces,
                "face_normals": self.face_normals}

    @classmethod
    def load(cls, file_obj):
        mesh, header = cls.READER(file_obj)
        return cls(**mesh, header=header)

    def export(self, file_obj):
        self.WRITER(file_obj, self)

    def __repr__(self):
        return f"{self.__class__.__name__}<n_vertices={self.header.vertex_count}, n_faces={self.header.face_count}>"





