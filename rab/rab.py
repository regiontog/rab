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
from utils import map_args, each
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

def create(paths):
    for path in paths:
        snapshot.set(path)
        snapshot.create()

def delete(paths):
    for path in paths:
        snapshot.set(path)
        snapshot.delete()

def recon(name, file, paths):
    snapshot.set(name)
    file = snapshot.File.from_path(file)
    file.reconstruct(paths[0])

def add(name, paths):
    snapshot.set(name)
    for path in each([p for p in paths]):
        Parse.parser(path)

def main():
    _setup()
    args = docopt(__doc__, version='rab version 0.1.1')

    if args['snapshot']:
        map_args(args, {'add'         : [add   , '<name>', 'PATH'] ,            # -> add(args['<name>'], args['PATH'])
                        'create'      : [create, 'PATH'] ,                      # -> create(args['PATH'])
                        'delete'      : [delete, 'PATH'] ,                      # -> delete(args['PATH'])
                        'reconstruct' : [recon , '<name>', '<file>', 'PATH']})  # -> recon(args['<name>'], args['<file>'], args['PATH'])

    elif args['blocks']:
        map_args(args, {'delete': [block.reset]})
