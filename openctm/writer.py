from . import compression

class CTMWriter:

    def __new__(cls, file_obj, ctm):
        try:
            # try to write to it
            return cls.write(file_obj, ctm)
        except AttributeError as e:
            # try to open it first
            with open(file_obj, 'wb') as file_obj:
                return cls.write(file_obj, ctm)

    @classmethod
    def write(cls, file_obj, ctm):
        # write ctm file
        cls.header(file_obj, ctm.header)
        cls.body(file_obj, ctm)

    @classmethod
    def header(cls, file_obj, header):
        file_obj.write(header.header.tobytes())

    @classmethod
    def body(cls, file_obj, ctm):

        transcoder = {b'MG1': compression.MG1,
                      b'MG2': compression.MG2}.get(ctm.header.compression_method, compression.RAW)

        transcoder.encode_body(file_obj, ctm)
