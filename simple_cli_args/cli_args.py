#!/usr/bin/env python3

import argparse
import inspect


#
class cli_args:
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

    def __init__(self, method):
        self.method = method
        self.__name__ = method.__name__
        self.__doc__ = method.__doc__
        self.build_argparser()

    def build_argparser(self):
        self.arg_spec = inspect.getfullargspec(self.method)
        self.n = len(self.arg_spec.args)
        self.positionals = self.n - len(self.arg_spec.defaults or '')
        self.module = inspect.getmodule(self.method)
        descriptions = filter(bool, [self.module.__doc__, self.method.__doc__])
        self.parser = argparse.ArgumentParser(
            description='\n'.join(descriptions),
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.add_positional_args()
        self.add_named_args()

    def add_positional_args(self):
        for i in range(self.positionals):
            arg = self.arg_spec.args[i]
            if i==0 and (arg in ['self', 'cls']):
                continue
            self.parser.add_argument(arg)

    def add_named_args(self):
        for i,j in enumerate(range(self.positionals, self.n)):
            arg = self.arg_spec.args[j]
            default = self.arg_spec.defaults[i]
            self.parser.add_argument(f'-{arg}', help=argparse.SUPPRESS,
                                     default=default)
            self.parser.add_argument(f'--{arg}', help=f'default: {default}',
                                     metavar=f'| -{arg[0]}  {arg.upper()}')

    def __call__(self, *args, **kwargs):
        if args or kwargs:
            return self.method(*args, **kwargs)
        # called blank()
        cli_arguments = self.parser.parse_args().__dict__
        return self.method(**cli_arguments)
