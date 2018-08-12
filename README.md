Python-OpenCTM
==============
[![Build Status](https://travis-ci.org/lejafar/Python-OpenCTM.svg?branch=master)](https://travis-ci.org/lejafar/Python-OpenCTM)
### Python Interface for the Open-CTM File Format

Python-OpenCTM is an (unofficial) Python interface for the [OpenCTM](https://github.com/Danny02/OpenCTM) file format. A format that allows a geometry to be compressed to a fraction of comparable file formats (3DS, STL, COLLADA...).

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
