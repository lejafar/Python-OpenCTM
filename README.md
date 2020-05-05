Python-OpenCTM
==============
![](https://github.com/lejafar/python-openctm/workflows/OpenCTM%20Release/badge.svg) [![PyPI version](https://badge.fury.io/py/python-openctm.svg)](https://badge.fury.io/py/python-openctm)
### Python Interface for the Open-CTM File Format

Python-OpenCTM is a Python interface for the [OpenCTM](https://github.com/Danny02/OpenCTM) file format. A format that allows a geometry to be compressed to a fraction of comparable file formats (3DS, STL, COLLADA...).

Pre-built python (**3.5**-**3.8**) wheels available for **Linux**, **MacOS** and **Windows**

## Installation

```shell
pip install python-openctm
```

## Usage

```python
import openctm

# read
mesh = openctm.import_mesh('foo.ctm')

print(mesh.vertices.shape)
# (124, 3)

# write
openctm.export_mesh(mesh, 'bar.ctm')
```
