""" Module docstring """

from unittest import TestCase, main
import sys
from io import StringIO

from simple_cli_args import cli_args


@cli_args
def plain_method(apple, pear, banana=9, *args, **kwargs):
    """ method docstring """
    return (apple, pear, banana, args, kwargs)


@cli_args
def no_args_method():
    return True


class TestAction(TestCase):

    def __init__(self, *args):
        TestCase.__init__(self, *args)
        self.method_to_test = plain_method

    def action(self, args):
        sys.argv = [''] + args.split()
        (self.apple, self.pear, self.banana, self.args,
         self.kwargs) = self.method_to_test()


class TestCliArgs(TestAction):

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
class TestCliArgsEmptyArgs(TestCase):

    def __init__(self, *args):
        TestCase.__init__(self, *args)
        self.method_to_test = no_args_method

    def action(self, args):
        sys.argv = [''] + args.split()
        self.result = self.method_to_test()

    def test_empty_call(self):
        self.action(args='')
        self.assertTrue(self.result)

    # TCs to be added


#
class TestHelp(TestAction):

    def test_both_docstrings(self):
        with CatchPrintout() as catch_print:
            self.assertRaises(SystemExit, self.action, args='-h')
            help_text = catch_print.getvalue()
        self.assertIn(" Module docstring \n method docstring", help_text)


#
class CatchPrintout(StringIO):

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self
        return self

    def __exit__(self, *args):
        sys.stdout = self._stdout


#
if __name__ == '__main__':
    main()
