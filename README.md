Python-OpenCTM (nightly)
==============
[![Build Status](https://travis-ci.org/lejafar/Python-OpenCTM.svg?branch=feature/nightly)](https://travis-ci.org/lejafar/Python-OpenCTM) [![PyPI version](https://badge.fury.io/py/python-openctm-nightly.svg)](https://badge.fury.io/py/python-openctm-nightly)
### Native Python Reader/Writer for the Open-CTM File Format

Python-OpenCTM is a native Python reader/writer for the [OpenCTM](https://github.com/Danny02/OpenCTM) file format. A format that allows a geometry to be compressed to a fraction of comparable file formats (3DS, STL, COLLADA...).

## Installation

```shell
pip install python-openctm-nightly
```

## Usage

```python
import openctm

# read
mesh = openctm.load('box.ctm')

print(mesh.vertices.shape)
# (12, 3)

# write
mesh.export('box.ctm')
```
