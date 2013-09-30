"""
Usage:
    rab snapshot create PATH...
    rab snapshot delete PATH...
    rab snapshot <name> add PATH...
    rab snapshot <name> reconstruct <file> PATH
    rab blocks delete
    rab [options] <command>... [<args>...]

Options:
    -h --help  Show this help message and quit.
    --version  Show version.

"""
import logging
from parse import Parse
from utils import map_args
from docopt import docopt
from database import block, snapshot
from utils import map_args, each, _setup

logger = logging.getLogger(__name__)

def create(paths):
    for path in paths:
        logger.info("Initializing snapshot %s" % path)
        snapshot.set(path)
        snapshot.create()

def delete(paths):
    for path in paths:
        logger.info("Clearing snapshot %s of all files" % path)
        snapshot.set(path)
        snapshot.delete()

def recon(name, file, paths):
    target = paths[0]
    logger.info("Reconstructing file %s from snapshot %s to %s" % (file, name, target))

    snapshot.set(name)
    file = snapshot.File.from_path(file)
    file.reconstruct(target)

def add(name, paths):
    snapshot.set(name)
    for path in each([p for p in paths]):
        logger.info("Adding file %s to snapshot %s" % (path, name))
        Parse.parser(path)

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

def main(argv):
    _setup()
    args = docopt(__doc__, version='rab version 0.1.1')
    logger.debug("Got args:\n%s", args)

    if args['snapshot']:
        map_args(args, {'add'         : [add   , '<name>', 'PATH'] ,            # -> add(args['<name>'], args['PATH'])
                        'create'      : [create, 'PATH'] ,                      # -> create(args['PATH'])
                        'delete'      : [delete, 'PATH'] ,                      # -> delete(args['PATH'])
                        'reconstruct' : [recon , '<name>', '<file>', 'PATH']})  # -> recon(args['<name>'], args['<file>'], args['PATH'])

    elif args['blocks']:
        map_args(args, {'delete': [block.reset]})
