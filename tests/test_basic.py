import pathlib
import numpy as np

import openctm

def test_basic_import_MG1():
    test_data = pathlib.Path(__file__).parent / 'test-data'
    file_path = test_data / 'squares.ctm'
    mesh = openctm.CTM.load(file_path)
    assert mesh.header.compression_method == b'MG1'
    assert mesh.vertices.shape == (124, 3)
    assert mesh.faces.shape == (284, 3)

def test_delta_encode_decode():
    data = np.array([[0, 1, 2], [2, 3, 4], [4, 5, 6], [6, 7, 8]]).reshape(-1)
    encoded_data = openctm.utils.delta_encode(data)
    decoded_data = openctm.utils.delta_decode(encoded_data)
    assert np.allclose(data, decoded_data)

