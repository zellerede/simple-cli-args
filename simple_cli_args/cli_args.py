#!/usr/bin/env python3

import argparse
import inspect
from termcolor import cprint


#
class cli_args:
    ''' Decorator for simple CLI argument parsing
        Method arguments without default value become positional
        and the other arguments get named

        Usage:

        # my_code.py

        @cli_args
        def main(x,y,z=8):
            """ This function is doing nice things. """
            print(x,y,z)

        main()  # parses the command line arguments, call e.g. by

        $  python3 my_code.py "Value for x" "Value for y" --z "Value for z"
    '''

    ERROR_MARKER = '-' * 40 + '\n'
    ERROR_COLOR = 'red'

    def __init__(self, method):
        self.method = method
        self.__name__ = method.__name__
        self.__doc__ = method.__doc__
        self.build_argparser()

    def build_argparser(self):
        self.arg_spec = inspect.getfullargspec(self.method)
        self.remove_leading_self_arg()
        self.n = len(self.arg_spec.args)
        self.positionals = self.n - len(self.arg_spec.defaults or '')
        self.additionals = self.arg_spec.varargs
        self.module = inspect.getmodule(self.method)
        descriptions = filter(bool, [self.module.__doc__, self.method.__doc__])
        self.parser = argparse.ArgumentParser(
            description='\n'.join(descriptions),
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.add_positional_args()
        self.add_named_args()
        self.add_additional_args()

    def remove_leading_self_arg(self):
        if self.arg_spec.args:
            leading_arg = self.arg_spec.args[0]
            if leading_arg in ['self', 'cls']:
                self.arg_spec.args.pop(0)

    def add_positional_args(self):
        for i in range(self.positionals):
            arg = self.arg_spec.args[i]
            self.parser.add_argument(arg)

    def add_named_args(self):
        for i,j in enumerate(range(self.positionals, self.n)):
            arg = self.arg_spec.args[j]
            default = self.arg_spec.defaults[i]
            self.parser.add_argument(
                f'-{arg}',
                help=argparse.SUPPRESS,
                default=default
            )
            self.parser.add_argument(
                f'--{arg}',
                help=f'default: {default}',
                metavar=f'| -{arg[0]}  {arg.upper()}'
            )

    def add_additional_args(self):
        if self.additionals:
            self.parser.add_argument(self.additionals, nargs='*')

    def get_call_args(self):
        if not self.additionals:
            return [], self.parser.parse_args().__dict__
        #
        known, additional = self.parser.parse_known_args()
        cli_kwargs = known.__dict__
        additional = cli_kwargs.pop(self.additionals, []) + additional
        cli_args = [cli_kwargs.pop(arg) for arg in self.arg_spec.args
                   ] + additional
        return cli_args, cli_kwargs

    def __call__(self, *args, **kwargs):
        if args or kwargs:
            return self.method(*args, **kwargs)
        # called blank()
        cli_args, cli_kwargs = self.get_call_args()
        try:
            return self.method(*cli_args, **cli_kwargs)
        except Exception as e:
            filename, lineno = self.get_error_info(e.__traceback__)
            self.print_err(self.ERROR_MARKER)
            self.print_err(f"ERROR in {filename}, at line {lineno}: {e}")

    # bonus:
    def get_error_info(self, traceback):
        while traceback:
            last_traceback = traceback
            traceback = traceback.tb_next
        filename = last_traceback.tb_frame.f_code.co_filename
        lineno = last_traceback.tb_lineno
        return filename, lineno

    def print_err(self, *args):
        cprint(*args, color=self.ERROR_COLOR)
