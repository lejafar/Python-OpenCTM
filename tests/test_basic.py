import pathlib
import numpy as np
import trimesh
import pytest
import tempfile

from openctm import CTM, import_mesh, export_mesh


@pytest.fixture
def data_path():
    return pathlib.Path(__file__).parent / 'test-data'


@pytest.fixture
def tmp():
    with tempfile.TemporaryDirectory() as tmp:
        yield pathlib.Path(tmp)


def test_round_trip(data_path, tmp):
    box_path = data_path / 'box.stl'
    org_mesh = trimesh.load(str(box_path))

    # export org_mesh to ctm
    ctm = CTM(org_mesh.vertices, org_mesh.faces, org_mesh.face_normals)
    box_path_ctm = tmp / box_path.with_suffix('.ctm').name
    export_mesh(ctm, box_path_ctm)

    # import ctm to mesh
    mesh = import_mesh(box_path_ctm)
    assert mesh.vertices.shape == org_mesh.vertices.shape
    assert mesh.faces.shape == org_mesh.faces.shape
    assert mesh.normals.shape == org_mesh.face_normals.shape
