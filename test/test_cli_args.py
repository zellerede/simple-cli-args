""" Module docstring """

from unittest import TestCase
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from cli_args import cli_args


@cli_args
def plain_method(apple, pear, banana=9, *args, **kwargs):
    """ method docstring """
    return (apple, pear, banana, args, kwargs)


@cli_args
def no_args_method():
    return True


class TestAction(TestCase):

    def action(self, args):
        sys.argv = [''] + args.split()
        (self.apple, self.pear, self.banana, self.args,
         self.kwargs) = self.method_to_test()


class TestCliArgs(TestAction):

    def __init__(self, *args):
        TestAction.__init__(self, *args)
        self.method_to_test = plain_method

    def test_default_value(self):
        self.action(args='app pea')
        self.assertEqual(self.apple, 'app')
        self.assertEqual(self.pear, 'pea')
        self.assertEqual(self.banana, 9)

    def test_abbreviate_1(self):
        self.action(args='app pea -b ban')
        self.assertEqual(self.banana, 'ban')

    def test_abbreviate_2(self):
        self.action(args='app pea -bana ban')
        self.assertEqual(self.banana, 'ban')

    def test_abbreviate_3(self):
        self.action(args='app pea --ba=banu')
        self.assertEqual(self.banana, 'banu')

    def test_full_name(self):
        self.action(args='app pea --banana no')
        self.assertEqual(self.banana, 'no')


#
class TestCliArgsEmptyArgs(TestAction):

    def __init__(self, *args):
        TestAction.__init__(self, *args)
        self.method_to_test = no_args_method

    # TCs to be added
