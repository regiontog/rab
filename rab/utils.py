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
