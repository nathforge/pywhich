#!/usr/bin/python

"""
Pywhich: Displays the full path of a Python module.
         Only supports regular files, i.e unzipped.

e.g:
    $ pywhich lxml
    /usr/lib/python2.6/dist-packages/lxml/__init__.py
"""

import imp
import os
import sys

def get_module_path(module_name):
    segments = module_name.split('.')
    module_path = os.path.sep.join(segments[:-1])
    last_module_name = segments[-1]
    for path in sys.path:
        try:
            module_file, pathname, (suffix, mode, module_type) = \
                imp.find_module(last_module_name, [os.path.join(path, module_path)])
        except ImportError:
            pass
        else:
            if module_type == imp.PKG_DIRECTORY:
                pathname = os.path.join(pathname, '__init__.py')
            return pathname

if __name__ == '__main__':
    from optparse import Option, OptionParser
    
    parser = OptionParser(usage='%prog module [options]', option_list=(
        Option('-p', '--path', action='store_true', default=False),
    ))
    options, args = parser.parse_args()
    
    if len(args) < 1:
        parser.error('Expected a module name')
    elif len(args) > 1:
        parser.error('Too many arguments')
    
    module_name = args[0]
    
    path = get_module_path(module_name)
    if path:
        if options.path:
            print os.path.dirname(path)
        else:
            print path

