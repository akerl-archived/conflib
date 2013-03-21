#!/usr/bin/env python3

import conflib

Default = { 'alpha' : 1,
    'beta' : 'fish',
    'charlie' : [3, 'fish'],
}

Global = { 'beta' : 'gmail',
    'delta' : 17,
}

Local = { 'alpha' : 9,
    'epsilon' : 'chocolate'
}

Validate = {
    'alpha' : (lambda x: int(x)),
    'charlie' : list,
    'epsilon' : [('winner', 'chocolate', 'frog'), ('what', 'is', 'up')],
}


MyConf = conflib.Config(Default, Global, Local, validation_dict=Validate)

print(MyConf.options)

