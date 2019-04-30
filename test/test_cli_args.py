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


def another_method():
    """ another docstring """
    pass


def no_docstring_method():
    pass


class TestAction(TestCase):

    def action(self, method_to_test=plain_method, args=''):
        sys.argv = [''] + args.split()
        (self.apple, self.pear, self.banana, self.args,
         self.kwargs) = method_to_test()


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
class TestCliArgsEmptyArgs(TestAction):

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

    class FakeModule:
        # no docstring
        pass

    def clear_module_docstring(self, method):
        method.__module__ = self.FakeModule
        return cli_args(method)

    def get_helptext(self, method=plain_method):
        with CatchPrintout() as catch_print:
            self.assertRaises(SystemExit, self.action, method, args='-h')
            self.help_text = catch_print.getvalue()

    def test_both_docstrings(self):
        self.get_helptext()
        self.assertIn(" Module docstring \n method docstring", self.help_text)

    def test_only_method_docstring(self):
        cli_method = self.clear_module_docstring(another_method)
        self.get_helptext(cli_method)
        self.assertNotIn("Module docstring", self.help_text)
        self.assertIn(" another docstring", self.help_text)
        self.assertEqual(self.help_text.count("docstring"), 1)

    def test_only_module_docstring(self):
        self.get_helptext(no_args_method)
        self.assertIn(" Module docstring", self.help_text)
        self.assertEqual(self.help_text.count("docstring"), 1)

    def test_no_docstring(self):
        cli_method = self.clear_module_docstring(no_docstring_method)
        self.get_helptext(cli_method)
        self.assertNotIn("docstring", self.help_text)

    def test_arguments(self):
        self.get_helptext()
        self.assertIn('apple pear', self.help_text)
        self.assertIn('--banana | -b  BANANA', self.help_text)


class TestProperties(TestCase):

    def test_method_names(self):
        self.assertEqual(plain_method.__name__, 'plain_method')
        self.assertEqual(no_args_method.__name__, 'no_args_method')

    def test_method_docstring(self):
        self.assertEqual(plain_method.__doc__, ' method docstring ')
        self.assertFalse(no_args_method.__doc__)


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
