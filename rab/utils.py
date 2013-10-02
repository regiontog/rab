import os
def map_args(args, functions):
    """Take a dict args and dict functions,
       iterate functions and if key exists in args
       and args[key] evaluates to True: run function
       from dict with its arguments

       format:
           functions = {'name': [fn, 'arg1', 'arg2']}
           args = {'name': True,
                   'arg1': 'Hello',
                   'arg2': 'World'}

       Would result in: fn('Hello', 'World')
    """
    def conv(arg_list):
        for arg in arg_list:
            yield args[arg]

    for key, val in functions.iteritems():
        if args[key]:
            fn = val.pop(0)
            new = conv(val)
            if new:
                fn(*new)
            else:
                fn()

def each(paths):
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for basename in files:
                    yield os.path.join(root, basename)
        else:
            yield path

def _setup():
    import sys
    import rabin
    import logging

    file = logging.FileHandler("/home/alan/.rab/log")
    file.setFormatter(logging.Formatter("%(levelname)s: %(asctime)s - %(name)s --  %(message)s"))
    file.setLevel(logging.DEBUG)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter("%(message)s"))
    console.setLevel(logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console)
    logger.addHandler(file)

    logging.getLogger(__name__).debug("===========")
    logging.getLogger(__name__).debug("Staring up.")
    logging.getLogger(__name__).debug("===========")

    kb = 1024
    rabin.set_window_size(48)
    rabin.set_min_block_size(8*kb)
    rabin.set_average_block_size(64*kb-1)
    rabin.set_max_block_size(256*kb)
