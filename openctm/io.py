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

def load_ctm(file_obj, file_type=None):
    """
    Load OpenCTM files from a file object.
    Parameters
    ----------
    file_obj : open file- like object
    Returns
    ----------
    loaded : dict
              kwargs for a Trimesh constructor:
                {vertices: (n,3) float, vertices
                 faces:    (m,3) int, indexes of vertices}
    """

    # !!load file from name
    # this should be replaced with something that
    # actually uses the file object data to support streams
    name = str(file_obj.name).encode('utf-8')

    with open_ctm(name) as ctm_file:
        vertices = ctm_file.get_vertices()
        faces = ctm_file.get_faces()

        # create kwargs for trimesh constructor
        result = {'vertices': vertices,
                  'faces': faces}

        # get face normals if available
        face_normals = ctm_file.get_face_normals()
        if face_normals:
            result['face_normals'] = face_normals

    return result
