# python-ctm
### Python Interface for the Open-CTM Library

Python-CTM is an (unofficial) Python interface for the [OpenCTM](https://github.com/Danny02/OpenCTM) file format. A format that allows a geometry to be compressed to a fraction of comparable file formats (3DS, STL, COLLADA...).

## Installation

```shell
pip install python-ctm
```

## Usage

```python
with open_ctm(name) as ctm_file:
  vertices = ctm_file.get_vertices()
  faces = ctm_file.get_faces()

  result = {'vertices': vertices,
            'faces': faces}

  # get face normals if available
  face_normals = ctm_file.get_face_normals()
  if face_normals:
      result['face_normals'] = face_normals
```
