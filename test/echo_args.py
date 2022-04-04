#!/usr/bin/env python3
# from simple_cli_args import cli_args

from pathlib import Path
from importlib.machinery import SourceFileLoader
simple_cli_args = SourceFileLoader('simple_cli_args',
    str(Path(__file__).absolute().parent.parent / 'simple_cli_args' / '__init__.py')
).load_module()
cli_args = simple_cli_args.cli_args

@cli_args
def main(apple, banana, cucumber='green', *others):
    print("Our fruits are:", apple, banana, cucumber, '|', ', '.join(others))

if __name__ == '__main__':
    main()
