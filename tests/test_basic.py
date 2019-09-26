import pathlib
import numpy as np
import trimesh

import openctm

def data_path(): return pathlib.Path(__file__).parent / 'test-data'

def test_basic_import_MG1():
    mesh = openctm.CTM.load(data_path() / 'squares.ctm')

    assert mesh.header.compression_method == b'MG1'
    assert mesh.vertices.shape == (124, 3)
    assert mesh.faces.shape == (284, 3)

def test_import_MG1_export_RAW_import_RAW():
    # import MG1
    mesh_MG1 = openctm.CTM.load(data_path() / 'squares.ctm')

    # export RAW
    mesh_MG1.header.compression_method = "RAW"
    mesh_MG1.export(data_path() / 'squares_RAW.ctm')

    # import RAW
    mesh_RAW = openctm.CTM.load(data_path() / 'squares_RAW.ctm')

    assert mesh_MG1.vertices.shape == mesh_RAW.vertices.shape
    assert mesh_MG1.faces.shape == mesh_RAW.faces.shape

    assert np.allclose(mesh_MG1.vertices, mesh_RAW.vertices)
    assert np.allclose(mesh_MG1.faces, mesh_RAW.faces)

def test_round_trip():
    mesh = trimesh.load(str(data_path() / 'box.stl'))

    # export-import
    ctm = openctm.CTM(mesh.vertices, mesh.faces)
    ctm.export(data_path() / 'box.ctm')
    ctm = openctm.CTM.load(data_path() / 'box.ctm')

    assert mesh.vertices.shape == ctm.vertices.shape
    assert mesh.faces.shape == ctm.faces.shape


def test_delta_encode_decode():
    data = np.array([[0, 1, 2], [2, 3, 4], [4, 5, 6], [6, 7, 8]]).reshape(-1)
    encoded_data = openctm.utils.delta_encode(data)
    decoded_data = openctm.utils.delta_decode(encoded_data)
    assert np.allclose(data, decoded_data)

