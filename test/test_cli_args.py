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


class ClassForClassMethod:

    @cli_args
    def class_method(self, apple, pear, banana=9, *args, **kwargs):
        """ method docstring """
        self.apple = apple
        self.pear = pear
        self.banana = banana
        self.args = args
        self.kwargs = kwargs

    @cli_args
    def class_no_args_method(self):
        return True


class TestCliArgs(TestCase):

    def action(self, args):
        sys.argv = [''] + args.split()
        (self.apple, self.pear, self.banana, self.args,
         self.kwargs) = plain_method()

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


#class TestClassMethod(TestCase, ClassForClassMethod):
