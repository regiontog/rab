import os
import rabin
from parse import Parse

def _setup():
    kb = 1024
    rabin.set_window_size(48)
    rabin.set_min_block_size(8*kb)
    rabin.set_average_block_size(64*kb-1)
    rabin.set_max_block_size(256*kb)

    Parse.rab = rabin.Rabin()
    Parse.rab.register(Parse._block_reached)

def main(argv):
    fname = argv.pop(0)
    paths = argv
    _setup()

    for path in each(paths):
        Parse.parser(path)

def each(paths):
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for basename in files:
                    yield os.path.join(root, basename)
        else:
            yield path
