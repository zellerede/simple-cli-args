""" Module docstring """

from unittest import TestCase, main
import sys
from pathlib import Path
from io import StringIO

from importlib.machinery import SourceFileLoader
simple_cli_args = SourceFileLoader('simple_cli_args',
    str(Path(__file__).absolute().parent.parent / 'simple_cli_args' / '__init__.py')
).load_module()
cli_args = simple_cli_args.cli_args

sys.argv = ['my_cli.py']


@cli_args
def no_args_method():
    return True


@cli_args
def plain_method(apple, pear, banana=9):
    """ method docstring """
    return (apple, pear, banana)


@cli_args
def full_method(apple, pear, banana=9, *args, **kwargs):
    """ methody docstring """
    return (apple, pear, banana, args, kwargs)

@cli_args
class PureClass:
    """ Class docstring """

    def __init__(self, apple, pear, banana=9):
        """ even constructor docstring """
        self.fruits = (apple, pear, banana)


@cli_args
class MainClass:
    """ Class docstring """

    def __init__(self, apple, pear, banana=9, *args, **kwargs):
        """ even constructor docstring """
        self.fruits = (apple, pear, banana, args, kwargs)


def another_method():
    """ another docstring """
    pass


@cli_args
def no_docstring_method():
    pass


class TestAction(TestCase):
    default_method = staticmethod(plain_method)

    def action(self, method_to_test=None, args=''):
        if method_to_test is None:
            method_to_test = self.default_method

        sys.argv = ['my_cli.py'] + args.split()
        self.result = method_to_test()
        if self.result not in (None, True):
            (self.apple, self.pear, self.banana, *rest) = self.result
            if rest:
                self.args = rest[0]


class TestCliArgs(TestAction):
    """ plain_method(apple, pear, banana=9) """

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

    def test_empty_call(self):
        self.action(no_args_method, args='')
        self.assertTrue(self.result)

    def test_nonempty_call(self):
        with CatchPrintout('stderr') as catch_print:
            with self.assertRaises(SystemExit) as problematic:
                self.action(no_args_method, args='elias tobias')
                self.assertEqual(problematic.exception.message, 2)
            message = catch_print.getvalue()
        self.assertIn('usage: my_cli.py [-h]', message)
        self.assertIn('error: unrecognized arguments: elias tobias', message)


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
        self.get_helptext(plain_method)
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
        self.get_helptext(plain_method)
        self.assertIn('apple pear', self.help_text)
        self.assertIn('--banana | -b  BANANA', self.help_text)

    def test_list_arguments(self):
        self.get_helptext(full_method)
        self.assertIn('[args [args ...]]', self.help_text)


class TestProperties(TestCase):

    def test_method_names(self):
        self.assertEqual(plain_method.__name__, 'plain_method')
        self.assertEqual(no_args_method.__name__, 'no_args_method')

    def test_method_docstring(self):
        self.assertEqual(plain_method.__doc__, ' method docstring ')
        self.assertFalse(no_args_method.__doc__)


#
class TestAdditionalArgs(TestAction):

    default_method = staticmethod(full_method)

    def test_additional_arg1(self):
        self.action(args='app pea lem pin')
        self.assertEqual(self.apple, 'app')
        self.assertEqual(self.pear, 'pea')
        self.assertEqual(self.banana, 9)
        self.assertEqual(self.args, ('lem', 'pin'))

    def test_additional_arg2(self):
        self.action(args='app pea lem --bana na mon pin eap ple')
        self.assertEqual(self.apple, 'app')
        self.assertEqual(self.pear, 'pea')
        self.assertEqual(self.banana, 'na')
        self.assertEqual(self.args, ('lem', 'mon', 'pin', 'eap', 'ple'))

    def test_additional_arg3(self):
        self.action(args='app --ban=ana pea EOF')
        self.assertEqual(self.apple, 'app')
        self.assertEqual(self.pear, 'pea')
        self.assertEqual(self.banana, 'ana')
        self.assertEqual(self.args, ('EOF',))

    def test_additional_arg4(self):
        self.action(args='-ba nana app pea')
        self.assertEqual(self.apple, 'app')
        self.assertEqual(self.pear, 'pea')
        self.assertEqual(self.banana, 'nana')
        self.assertFalse(self.args)


#
class TestCliArgsPureClass(TestCliArgs):
    def default_method(self):
        return PureClass().fruits


class TestCliArgsMainClass(TestCliArgs, TestAdditionalArgs):
    def default_method(self):
        return MainClass().fruits


#
class CatchPrintout(StringIO):

    def __init__(self, channel='stdout'):
        StringIO.__init__(self)
        self.channel = channel

    def __enter__(self):
        self._orig = getattr(sys, self.channel)
        setattr(sys, self.channel, self)
        return self

    def __exit__(self, *args):
        setattr(sys, self.channel, self._orig)


#
if __name__ == '__main__':
    main()
