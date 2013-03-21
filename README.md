conflib - Configuration hierarchies made --easy-- easier
=====

Overview
-----

This module is designed to simplify the management of configurations. Primarily, this was written to allow easy ststacking of default, global, and local settings. It also handles validation of settings so you can confirm that user input looks like it's supposed to.

How to use
-----

    import conflib
    
    defaults = {'hello': 'world', 'alpha': 5}
    globals = {'wat': 'wut', 'fancy': (20, 'fish')}
    locals = {'hello': 'everybody', 'beta': 'qwerty'}
    
    validator = {
        'alpha': lambda x: x < 10,
        'fancy': tuple,
        'beta': [{'asdf', 'qwerty'}, {'fizz','buzz'}]
    }
    
    my_config = conflib.Config(defaults, globals, locals)
    print(my_config.options)

