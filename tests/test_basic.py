import unittest
import os

from openctm import import_mesh, export_mesh


class BasicTestSuiteFunctions(unittest.TestCase):

    def setUp(self):
        self.file_dir = "tests/test-data/"

    def testImportVertices(self):
        mesh = import_mesh("%s/squares.ctm" % self.file_dir)
        assert len(mesh.vertices) == 124

    def testImportFaces(self):
        mesh = import_mesh("%s/squares.ctm" % self.file_dir)
        assert len(mesh.faces) == 284

    def testExportImport(self):
        original_mesh = import_mesh("%s/squares.ctm" % self.file_dir)
        export_mesh(original_mesh, "%s/squares_exported.ctm" % self.file_dir)

        exported_mesh = import_mesh("%s/squares_exported.ctm" % self.file_dir)

        assert original_mesh == exported_mesh
        os.remove("%s/squares_exported.ctm" % self.file_dir)


if __name__ == '__main__':
    unittest.main()
