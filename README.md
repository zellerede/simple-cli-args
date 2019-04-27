# simple-cli-args
A python main method decorator.<br>
An enhancement of the `argparse` package for its simplest usages.

The ordinary arguments become positional, the arguments with default value become named argument for the CLI, 
with a possibility of abbreviations, as `argparse` provides it.<br>
Help option (`-h` or `--help`) is automatically generated with its text taken from the docstrings.

### Install

#### Using pip
    pip install simple_cli_args

or, with your intended python command in place of `python`

    python -m pip install simple_cli_args

#### Using setuptools
Simply issue in the main directory of the cloned git repository:

    ./setup.py install

### Usage
Assume the content of *my_cli.py* is:

    #!/usr/bin/env python3
    from simple_cli_args import cli_args
    
    @cli_args
    def main(apple, banana, cucumber='green'):
        print("Our fruits are:", apple, banana, cucumber)
    
    if __name__ == '__main__':
        main()  # without arguments given, those will be read from the CLI

Then, we get the following printouts:

    $ ./my_cli.py red yellow
    Our fruits are: red yellow green

    $ ./my_cli.py red yellow --cucumber=purple
    Our fruits are: red yellow purple

    $ ./my_cli.py red yellow -c nice
    Our fruits are: red yellow nice

    $ ./my_cli.py red
    usage: my_cli.py [-h] [--cucumber | -c  CUCUMBER] apple banana
    my_cli.py: error: the following arguments are required: banana

    $ ./my_cli.py --help
    usage: my_cli.py [-h] [--cucumber | -c  CUCUMBER] apple banana
    
    positional arguments:
      apple
      banana
    
    optional arguments:
      -h, --help            show this help message and exit
      --cucumber | -c  CUCUMBER
                            default: 42
    