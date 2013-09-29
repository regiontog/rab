from database import snapshot, block
import os

class Parse:
    data = ""
    rab = None
    path = None
    buffer_size = 1024

    @staticmethod
    def parser(path):
        Parse.data = ""
        Parse.path = path

        if os.access(path, os.R_OK):
            with open(path, 'rb') as file:
                Parse._read_file(file)

        else:
            print "No read access on file", path

    @staticmethod
    def _read_file(file):
        while "read":
            chunk = file.read(Parse.buffer_size)
            if chunk:
                Parse.data = ''.join([Parse.data, chunk])
                Parse.rab.update(chunk)
            else:   #EOF
                Parse._flush()
                break

    @staticmethod
    def _block_reached(offset, size, fp):
        dblock = block.Block.with_blob(Parse.data[:size], size)
        dbfile = snapshot.File.from_path(Parse.path)

        dblock.store()
        dbfile.add_block(offset, dblock)

        Parse.data = Parse.data[size:]

    @staticmethod
    def _flush():
        remaining = len(Parse.data)
        offset = os.path.getsize(Parse.path) - remaining

        Parse._block_reached(offset, remaining, None)
