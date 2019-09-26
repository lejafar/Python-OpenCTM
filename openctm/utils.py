import struct
import numpy as np
import lzma
import zlib

def read_uint_16(file_obj):
    return struct.unpack('H', file_obj.read(2))[0]

def write_uint_16(file_obj, integer):
    file_obj.write(struct.pack('H', integer))

def read_int_32(file_obj):
    return struct.unpack('i', file_obj.read(4))[0]

def write_int_32(file_obj, integer):
    file_obj.write(struct.pack('i', integer))

def read_string(file_obj, size=None):
    size = size or read_int_32(file_obj)
    if size:
        return "".join([chr(ord(read_char(file_obj))) for _ in range(size)])
    return ""

def write_string(file_obj, string):
    file_obj.write(struct.pack("{0}s".format(len(string)), str.encode(string)))

def read_char(file_obj):
    return struct.unpack('s', file_obj.read(1))[0]

def write_char(file_obj, char):
    file_obj.write(struct.pack('s', char))

def read_int_32_array(file_obj, length):
    return np.frombuffer(file_obj.read(4*length), dtype=np.int32, count=length)

def write_int_32_array(file_obj, array):
    file_obj.write(array.astype(np.int32).tobytes())

def read_float_32_array(file_obj, length):
    return np.frombuffer(file_obj.read(4*length), dtype=np.float32, count=length)

def write_float_32_array(file_obj, array):
    file_obj.write(array.astype(np.float32).tobytes())

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

def write_packed_data(file_obj, data, stride=3):

    lc = 3
    lp = 0
    pb = 2

    dict_size = 65536

    comp_filters = [{"id": lzma.FILTER_LZMA1, "dict_size": dict_size, "lc": lc, "lp": lp, "pb": pb}]
    # create numpy array containing all separate bytes and apply byte interleaving
    non_interleaved = np.frombuffer(data, dtype=np.dtype('b'), count=len(data) * 4)
    interleaved = np.flip(non_interleaved.reshape(-1, stride, 4), 0).reshape(-1, order='F')

    compressed_data = compress_lzma(interleaved, filters=comp_filters)
    packed_size = write_int_32(file_obj, len(compressed_data))

    # to be continued ...

def read_packed_data_zlib(file_obj, packed_size, dtype, element_count):
    decompressed = zlib.decompress(file_obj.read(packed_size))
    return np.frombuffer(decompressed, dtype=dtype, count=element_count)

def write_packed_data_zlib(file_obj, data):
    compressed = zlib.compress(data.tobytes())
    # write packed data length
    write_int_32(file_obj, len(compressed))
    # write packed data
    file_obj.write(compressed)

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

def compress_lzma(data, filters=None):
    results = []

    while True:
        comp = lzma.LZMACompressor(format=lzma.FORMAT_RAW, filters=filters)
        break
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

def delta_encode(data):

    encoded_data = np.copy(data)
    if len(encoded_data) > 0:
        encoded_data[1] -= data[0]
        encoded_data[2] -= data[0]

    for i in range(3, len(encoded_data), 3):
        encoded_data[i] -= data[i - 3]

        if data[i] == data[i - 3]:
            encoded_data[i + 1] -= data[i - 2]
        else:
            encoded_data[i + 1] -= data[i]

        encoded_data[i + 2] -= data[i]

    return encoded_data

