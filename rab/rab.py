import os
import rabin
import database as db

kb = 1024
buffer_size = 1*kb
rabin.set_window_size(48)
rabin.set_min_block_size(8*kb)
rabin.set_average_block_size(64*kb-1)
rabin.set_max_block_size(256*kb)


def main(argv):
    fname = argv.pop(0)
    paths = argv

    for file in each(paths):
        read_file(file)

def each(paths):
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for basename in files:
                    yield os.path.join(root, basename)
        else:
            yield path


def read_file(file):
    blob = {'data':''} ##Fix: nonlocal workaround
    def block_reached(offset, size, fp):
        head = blob["data"][:size]
        tail = blob["data"][size:]
        blob["data"] = tail

        block   = db.Block.from_blob(head, size)
        db_file = db.File.from_path(file)

        if not block.exists():
            block.store()
            print "Inserting", block
        else:
            print "-----> Block", block, "already exists"

        db_file.add_block(offset, block)


    r = rabin.Rabin()
    r.register(block_reached)

    if os.access(file, os.R_OK):
        with open(file, 'rb') as f:
            while "read":
                data = f.read(buffer_size)
                if not data: break
                blob['data'] = ''.join([blob["data"], data])
                r.update(data)

            block_reached(os.path.getsize(file)-len(blob['data']), len(blob['data']), None)
    else:
        print "No read access on file", file
