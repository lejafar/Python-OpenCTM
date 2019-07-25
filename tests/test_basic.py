import pathlib

import openctm

def test_basic_import_MG1():
    file_path = (pathlib.Path(__file__).parent / 'test-data') / 'squares.ctm'
    mesh = openctm.CTM(file_path)
    assert mesh.header.compression_method == b'MG1'
    assert mesh.vertices.shape == (124, 3)
    assert mesh.faces.shape == (284, 3)
