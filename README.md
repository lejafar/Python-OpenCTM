# python-ctm
### Python Interface for the Open-CTM Library

Python-CTM is an (unofficial) Python interface for the [OpenCTM](https://github.com/Danny02/OpenCTM) file format, software library and tool set for compression of 3D triangle meshes . The format allows a geometry to be compressed to a fraction of comparable file formats (3DS, STL, COLLADA...), and is accessible through a simple, portable API.

This package currently supports:
* __Reading__: OpenCTM file into a numpy array.
* __Writing__: a numpy array to an OpenCTM file.

## Installation

In order to install the Python wrappers for OpenCTM, simply run
```shell
pip install python-ctm
```
