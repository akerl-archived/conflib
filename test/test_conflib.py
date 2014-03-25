import unittest
import nose
import conflib


class TestConflib:
    def test_creation(self):
        config = conflib.Config()
        assert type(config) is conflib.Config
        assert config.options == {}

    def test_population(self):
        test = {'foo': 5, 'bar': 10}
        config = conflib.Config(test)
        assert config.options == test

    def test_stacking(self):
        a = {'foo': 5, 'bar': 10}
        b = {'foo': 'alpha', 'baz': 15}
        config = conflib.Config(a, b)
        assert config.options == {'foo': 'alpha', 'bar': 10, 'baz': 15}

    def test_delayed_stacking(self):
        a = {'foo': 5, 'bar': 10}
        b = {'foo': 'alpha', 'baz': 15}
        config = conflib.Config(a)
        config.stack(b)
        assert config.options == {'foo': 'alpha', 'bar': 10, 'baz': 15}

    def test_conflib_stacking(self):
        a = conflib.Config({'foo': 'bar', 'fizz': 'buzz'})
        b = conflib.Config({'foo': 'who', 'wat': 'wut'})
        a.stack(b)
        assert a.options == {'foo': 'who', 'fizz': 'buzz', 'wat': 'wut'}
        assert type(b) is conflib.Config

    def test_validation_bool(self):
        values = {
            'a': 'y',
            'b': 'yes',
            'c': '1',
            'd': 1,
            'e': True,
            'f': 'n',
            'g': 'no',
            'h': '0',
            'i': 0,
            'j': False,
        }
        validation = {
            'a': bool,
            'b': bool,
            'c': bool,
            'd': bool,
            'e': bool,
            'f': bool,
            'g': bool,
            'h': bool,
            'i': bool,
            'j': bool,
        }
        results = {
            'a': True,
            'b': True,
            'c': True,
            'd': True,
            'e': True,
            'f': False,
            'g': False,
            'h': False,
            'i': False,
            'j': False,
        }
        config = conflib.Config(values, validation_dict=validation)
        assert config.options == results

    @nose.tools.raises(ValueError)
    def test_validation_bool_fail(self):
        values = {
            'a': 'f',
        }
        validation = {
            'a': bool,
        }
        conflib.Config(values, validation_dict=validation)

    def test_validation_int(self):
        values = {
            'a': 1,
            'b': '2',
            'c': 5.4,
        }
        validation = {
            'a': int,
            'b': int,
            'c': int,
        }
        results = {
            'a': 1,
            'b': 2,
            'c': 5,
        }
        config = conflib.Config(values, validation_dict=validation)
        assert config.options == results

    @nose.tools.raises(ValueError)
    def test_validation_int_fail(self):
        values = {
            'a': 'foo',
        }
        validation = {
            'a': int,
        }
        conflib.Config(values, validation_dict=validation)

    def test_validation_list(self):
        values = {
            'a': 'foo',
            'b': 'bar',
        }
        validation = {
            'a': ['whiz', 'bang', 'foo', 'buzz'],
            'b': [('fizz', 'bar'), ('wat', 'wut')],
        }
        results = {
            'a': 'foo',
            'b': 'fizz',
        }
        config = conflib.Config(values, validation_dict=validation)
        assert config.options == results

    @nose.tools.raises(ValueError)
    def test_validation_list_fail(self):
        values = {
            'a': 'bar'
        }
        validation = {
            'a': ['what', 'wut', 'wat'],
        }
        conflib.Config(values, validation_dict=validation)

    def test_validation_types(self):
        config = conflib.Config()
        values = {
            'a': 'fish',
            'b': config,
        }
        validation = {
            'a': str,
            'b': conflib.Config,
        }
        results = {
            'a': 'fish',
            'b': config,
        }
        config = conflib.Config(values, validation_dict=validation)
        assert config.options == results

    @nose.tools.raises(ValueError)
    def test_validation_types_fail(self):
        values = {
            'a': 5,
        }
        validation = {
            'a': float,
        }
        conflib.Config(values, validation_dict=validation)

    def test_validation_callable(self):
        values = {
            'a': 10,
        }
        validation = {
            'a': lambda x: x / 2,
        }
        results = {
            'a': 5,
        }
        config = conflib.Config(values, validation_dict=validation)
        assert config.options == results

    @nose.tools.raises(ValueError)
    def test_validation_callable_fail(self):
        def raise_it(x):
            if x != 5:
                raise ValueError
        values = {
            'a': 10,
        }
        validation = {
            'a': lambda x: raise_it(x),
        }
        conflib.Config(values, validation_dict=validation)

    @nose.tools.raises(ValueError)
    def test_validation_fail(self):
        values = {
            'a': 10,
        }
        validation = {
            'a': 'other'
        }
        conflib.Config(values, validation_dict=validation)
