from database import snapshot, block
import logging
import rabin
import os

logger = logging.getLogger(__name__)

class Parse:
    data = ""
    path = None
    buffer_size = 1024

    rab = rabin.Rabin()

    @staticmethod
    def parser(path):
        Parse.data = ""
        Parse.path = path
        Parse.rab.register(Parse._block_reached)

        if os.access(path, os.R_OK):
            with open(path, 'rb') as file:
                Parse._read_file(file)

        else:
            logger.warn("No read access on file %s" % path)

    @staticmethod
    def _read_file(file):
        logger.debug("Reading file %s" % file)
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
        logger.debug("Got chunk with offset %s, fingerprint %s, size %s" % (offset, hex(int(fp)), size))

        dblock = block.Block.with_blob(Parse.data[:size], size)
        dbfile = snapshot.File.from_path(Parse.path)

        dblock.store()
        dbfile.add_block(offset, dblock)

        Parse.data = Parse.data[size:]

    @staticmethod
    def _flush():
        remaining = len(Parse.data)
        offset = os.path.getsize(Parse.path) - remaining

        Parse._block_reached(offset, remaining, 0)
