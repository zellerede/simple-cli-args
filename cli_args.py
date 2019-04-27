#!/usr/bin/env python3

import argparse
import inspect


#
def cli_args(method):
    ''' Decorator for simple CLI argument parsing
        Method arguments without default value become positional
        and the other arguments get named

        Usage:

        @cli_args
        def main(x,y,z=8):
            """ This function is doing nice things. """
            print(x,y,z)

        main()  # parses the command line arguments, call e.g. by

        >  my_code.py "Value for x" "Value for y" --z "Value for z"
    '''
    arg_spec = inspect.getfullargspec(method)
    n = len(arg_spec.args)
    positionals = n - len(arg_spec.defaults or '')
    module = inspect.getmodule(method)
    descriptions = filter(bool, [module.__doc__, method.__doc__])
    parser = argparse.ArgumentParser(
        description='\n'.join(descriptions),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    for i in range(positionals):
        arg = arg_spec.args[i]
        if i==0 and (arg in ['self', 'cls']):
            continue
        parser.add_argument(arg)
    for i in range(positionals, n):
        arg = arg_spec.args[i]
        default=arg_spec.defaults[i - positionals]
        parser.add_argument(f'-{arg}', help=argparse.SUPPRESS, default=default)
        parser.add_argument(f'--{arg}', metavar=f'| -{arg[0]}  {arg.upper()}',
                            help=f'default: {default}')

    def decorated(*args, **kwargs):
        if args or kwargs:
            return method(*args, **kwargs)
        # called blank()
        cli_arguments = parser.parse_args().__dict__
        return method(**cli_arguments)

    decorated.__name__ = method.__name__
    decorated.__doc__ = method.__doc__
    return decorated
