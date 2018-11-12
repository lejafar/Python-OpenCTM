"""
Copyright (c) 2018 Rafael Hautekiet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
References:
- "OpenCTM: The Open Compressed Triangle Mesh file format" by Marcus Geelnard
  http://openctm.sourceforge.net/
"""


import struct
import numpy as np
import lzma
import box

RAW=0x00574152
MG1=0x0031474d
MG2=0x0032474d

NORMALS=0x00000001

_ctm_header_type = np.dtype([('magic_identifier', np.dtype('S4')),
                             ('file_format', np.dtype('<i4')),
                             ('compression_method', np.dtype('S4')),
                             ('vertex_count', np.dtype('<i4')),
                             ('face_count', np.dtype('<i4')),
                             ('uv_map_count', np.dtype('<i4')),
                             ('attr_map_count', np.dtype('<i4')),
                             ('flags', np.dtype('<i4'))])

def read_int_32(file_obj):
    return struct.unpack('i', file_obj.read(4))[0]

def read_string(file_obj):
    size = read_int_32(file_obj)
    if size:
    	return struct.unpack('s', file_obj.read(size))[0]
    return ""

def read_int_32_array(file_obj, length):
    return np.frombuffer(file_obj.read(4*length), dtype=np.int32, count=length)

def read_float_32_array(file_obj, length):
    return np.frombuffer(file_obj.read(4*length), dtype=np.float32, count=length)

def read_ctm_header(file_obj):
    header = np.frombuffer(file_obj.read(_ctm_header_type.itemsize), dtype=_ctm_header_type)
    header = box.Box({k: header[k][0] for k in header.dtype.names})
    comment = read_string(file_obj)
    return header, comment

def read_ctm(file_obj):
    header, comment  = read_ctm_header(file_obj)

    if header.compression_method.decode('utf8') == "RAW":
        raise Exception("Not implemented yet!")

    if header.compression_method.decode('utf8') == "MG1":
        return read_ctm_MG1(file_obj, header)

    if header.compression_method.decode('utf8') == "MG2":
        raise Exception("Not implemented yet!")

def read_ctm_RAW(file_obj):
    return None

def read_ctm_MG1(file_obj, header):

    # Indices
    read_int_32(file_obj) # INDX
    indices = read_packed_data(file_obj, header.face_count, np.dtype('<i'), stride=3)
    indices = delta_decode(indices).reshape(-1,3)

    # Vertices
    read_int_32(file_obj) # VERT
    vertices = read_packed_data(file_obj, header.vertex_count, np.dtype('<f'), stride=1).reshape(-1,3)

    # Normals
    normals = None
    if header.flags & NORMALS:
        read_int_32(file_obj) # NORM
        normals = read_packed_data(file_obj, header.vertex_count, np.dtype('<f'), stride=3).reshape(-1,3)

    return indices, vertices, normals

def read_packed_data(file_obj, element_count, dtype, stride=3):

    packed_size = read_int_32(file_obj)

    # read LZMA properties
    lzma_props = file_obj.read(5)

    lzma_model_props = lzma_props[0]

    lc = lzma_model_props % 9 # the number of "literal context" bits
    lzma_model_props = (lzma_model_props - lc) // 9
    lp = lzma_model_props % 5 # the number of "literal pos" bits
    pb = (lzma_model_props - lp) // 5 # the number of "pos" bits

    dict_size = struct.unpack('i', lzma_props[1:])[0]

    comp_filters = [{"id": lzma.FILTER_LZMA1, "dict_size": dict_size, "lc": lc, "lp": lp, "pb": pb}]

    # decompress
    interleaved = decompress_lzma(file_obj.read(packed_size), filters=comp_filters)
    # create numpy array containing all separate bytes and undo byte level interleaving
    interleaved = np.frombuffer(interleaved, dtype=np.dtype('b'), count=element_count * 3 * 4)
    non_interleaved = np.flip(interleaved.reshape(4, stride, -1), 0).reshape(-1, order='F')

    return np.frombuffer(non_interleaved.tobytes(), dtype=dtype, count=element_count * 3)

#https://stackoverflow.com/a/37400585/8890398
def decompress_lzma(data, filters=None):
    results = []

    while True:
        decomp = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, memlimit=None, filters=filters)
        try:
            res = decomp.decompress(data)
        except lzma.LZMAError:
            if results:
                break  # Leftover data is not a valid LZMA/XZ stream
            else:
                raise  # Error on the first iteration
        results.append(res)
        data = decomp.unused_data
        if not data:
            break
        if not decomp.eof:
            raise lzma.LZMAError("Compressed data ended before the end-of-stream marker was reached")
    return b"".join(results)

def delta_decode(data):

    # TODO: replace by numpy operations
    decoded_data = np.copy(data)
    if len(decoded_data) > 0:
        decoded_data[2] += decoded_data[0]
        decoded_data[1] += decoded_data[0]

    for i in range(3, len(decoded_data), 3):
        decoded_data[i] += decoded_data[i - 3]

        if decoded_data[i] == decoded_data[i - 3]:
            decoded_data[i + 1] += decoded_data[i - 2]
        else:
            decoded_data[i + 1] += decoded_data[i]

        decoded_data[i + 2] += decoded_data[i]

    return decoded_data

