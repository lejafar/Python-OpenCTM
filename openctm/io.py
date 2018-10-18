from .openctm import *
import numpy as np


class CTM:
    """
    Object that encapsulates a CTM file
    """

    def __init__(self, _vertices, _faces, _normals=None):
        self.vertices = _vertices
        self.faces = _faces
        self.normals = _normals

    def __eq__(self, other):
        return (self.vertices == other.vertices).all() and (self.faces == other.faces).all()


def import_mesh(_filename):
    ctm_context = ctmNewContext(CTM_IMPORT)
    try:
        ctmLoad(ctm_context, _encode(_filename))
        err = ctmGetError(ctm_context)
        if err != CTM_NONE:
            raise IOError("Error loading file: %s" % str(ctmErrorString(err)))

        # read vertices
        vertex_count = ctmGetInteger(ctm_context, CTM_VERTEX_COUNT)
        vertex_ctm = ctmGetFloatArray(ctm_context, CTM_VERTICES)

        vertices = np.fromiter(vertex_ctm,
                               dtype=np.float,
                               count=vertex_count * 3).reshape((-1, 3))

        # read faces
        face_count = ctmGetInteger(ctm_context, CTM_TRIANGLE_COUNT)
        face_ctm = ctmGetIntegerArray(ctm_context, CTM_INDICES)
        faces = np.fromiter(face_ctm,
                            dtype=np.int,
                            count=face_count * 3).reshape((-1, 3))

        # read face normals
        normals = None
        if ctmGetInteger(ctm_context, CTM_HAS_NORMALS) == CTM_TRUE:
            normals_ctm = ctmGetFloatArray(ctm_context, CTM_NORMALS)
            normals = np.fromiter(normals_ctm,
                                  dtype=np.float,
                                  count=face_count * 3).reshape((-1, 3))
    finally:
        ctmFreeContext(ctm_context)

    return CTM(vertices, faces, normals)


def export_mesh(_ctm, _filename):
    ctm_context = ctmNewContext(CTM_EXPORT)
    
    if not str(_filename).lower().endswith('.ctm'):
        _filename += '.ctm'

    try:
        vertex_count = len(_ctm.vertices)
        vertices = _ctm.vertices.reshape((-1, 1))
        p_vertices = ctypes.cast((CTMfloat * vertex_count * 3)(), ctypes.POINTER(CTMfloat))
        for i in range(vertex_count * 3):
            p_vertices[i] = CTMfloat(vertices[i])

        face_count = len(_ctm.faces)
        faces = _ctm.faces.reshape((-1, 1))
        p_faces = ctypes.cast((CTMuint * face_count * 3)(), ctypes.POINTER(CTMuint))
        for i in range(face_count * 3):
            p_faces[i] = CTMuint(faces[i])

        if _ctm.normals is not None:
            normal_count = len(_ctm.normals)
            normals = _ctm.normals.reshape((-1, 1))
            p_normals = ctypes.cast((CTMfloat * normal_count * 3)(), ctypes.POINTER(CTMfloat))
            for i in range(normal_count * 3):
                p_normals[i] = CTMfloat(normals[i])
        else:
            p_normals = None

        ctmDefineMesh(ctm_context, p_vertices, CTMuint(vertex_count), p_faces, CTMuint(face_count), p_normals)
        ctmSave(ctm_context, ctypes.c_char_p(_encode(_filename)))
    finally:
        ctmFreeContext(ctm_context)

def _encode(_filename):
    try:
        return str(_filename).encode("utf-8")
    except UnicodeEncodeError:
        pass

    try:
        # works fine for pathlib.Path
        return bytes(_filename)
    except TypeError:
        pass

    return str(_filename).encode("utf-8", "surrogateescape")

