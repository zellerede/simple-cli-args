"""
    Usage example:

my_script.py:

    #!/usr/bin/env python

    from simple_cli_args import cli_args

    @cli_args
    def main(arg1, arg2, defarg1="def1", defarg2="def2", *otherargs, **kwargs)
        # use the arguments as strings
        print(arg1, arg2, defarg1, defarg2, otherargs, kwargs)

    if __name__ == '__main__':
        # note the empty argument list -> this invokes reading the cli arguments
        main()
"""

from .cli_args import cli_args
