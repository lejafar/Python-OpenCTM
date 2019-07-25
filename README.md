Python-OpenCTM (nightly)
==============
[![Build Status](https://travis-ci.org/lejafar/Python-OpenCTM.svg?branch=feature/nightly)](https://travis-ci.org/lejafar/Python-OpenCTM) [![PyPI version](https://badge.fury.io/py/python-openctm-nightly.svg)](https://badge.fury.io/py/python-openctm-nightly)
### Python Interface for the Open-CTM File Format

Python-OpenCTM is a Python interface for the [OpenCTM](https://github.com/Danny02/OpenCTM) file format. A format that allows a geometry to be compressed to a fraction of comparable file formats (3DS, STL, COLLADA...).

## Installation

```shell
pip install python-openctm-nightly
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
