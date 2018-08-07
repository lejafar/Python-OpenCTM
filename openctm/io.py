from .openctm import *
import numpy as np
from contextlib import contextmanager

@contextmanager
def open_ctm(filename):
    ctm_context = ctmNewContext(CTM_IMPORT)
    yield CtmFile(ctm_context, filename)
    ctmFreeContext(ctm_context)

class CtmFile:

    def __init__(self, ctm_context, filename):
        self.ctm = ctm_context
        ctmLoad(self.ctm, filename)
        err = ctmGetError(self.ctm)
        if err != CTM_NONE:
            raise IOError("Error loading file: " + str(ctmErrorString(err)))

    def get_vertices(self):
        # get vertices
        vertex_count = ctmGetInteger(self.ctm, CTM_VERTEX_COUNT)
        vertex_ctm = ctmGetFloatArray(self.ctm, CTM_VERTICES)
        # use fromiter to avoid loop
        vertices = np.fromiter(vertex_ctm,
                               dtype=np.float,
                               count=vertex_count * 3).reshape((-1, 3))
        return vertices

    def get_faces(self):
        # get faces
        face_count = ctmGetInteger(self.ctm, CTM_TRIANGLE_COUNT)
        face_ctm = ctmGetIntegerArray(self.ctm, CTM_INDICES)
        faces = np.fromiter(face_ctm,
                            dtype=np.int,
                            count=face_count * 3).reshape((-1, 3))
        return faces

    def get_face_normals(self):
        if ctmGetInteger(self.ctm, CTM_HAS_NORMALS) == CTM_TRUE:
            normals_ctm = ctmGetFloatArray(self.ctm, CTM_NORMALS)
            normals = np.fromiter(normals_ctm,
                                  dtype=np.float,
                                  count=face_count * 3).reshape((-1, 3))
            return normals
        # if not available return None
        else:
            return None
