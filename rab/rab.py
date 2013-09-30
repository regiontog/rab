"""
Usage:
    rab snapshot create PATH...
    rab snapshot delete PATH...
    rab snapshot <name> add PATH...
    rab snapshot <name> reconstruct <file> PATH
    rab blocks delete
    rab (--version | -h | --help)

Options:
    -h --help  Show this help message and quit.
    --version  Show version.

"""
import os
import rabin
from parse import Parse
from docopt import docopt
from database import block, snapshot

def _setup():
    kb = 1024
    rabin.set_window_size(48)
    rabin.set_min_block_size(8*kb)
    rabin.set_average_block_size(64*kb-1)
    rabin.set_max_block_size(256*kb)

    Parse.rab = rabin.Rabin()
    Parse.rab.register(Parse._block_reached)

def main(argv):
    _setup()

    args = docopt(__doc__, version='rab version 0.1.1')

    if args['snapshot']:
        if args['create']:
            for path in args['PATH']:
                snapshot.set(path)
                snapshot.create()

        elif args['delete']:
            for path in args['PATH']:
                snapshot.set(path)
                snapshot.delete()

        elif args['reconstruct']:
            snapshot.set(args['<name>'])
            file = snapshot.File.from_path(args['<file>'])
            file.reconstruct(args['PATH'][0])

        elif args['add']:
            snapshot.set(args['<name>'])
            for path in each([p for p in args['PATH']]):
                Parse.parser(path)

    elif args['blocks'] and args['delete']:
        block.reset()


def each(paths):
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for basename in files:
                    yield os.path.join(root, basename)
        else:
            yield path
