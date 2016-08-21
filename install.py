#!/usr/bin/python3

"""
One-run install of `dcore`.
"""

import sys
import os
import platform

import dcore.data as data
import dcore.create_python_scripts_shortcuts as create_python_scripts_shortcuts

def setupShortcutsBootstrap():
    """
    We put all shortcuts in dcore-owned directory and add it to executable PATH loaded by shell.
    """

    #:::replace with truly random.
    tag = "fh89h98h3f9hf39hf98ahsfd9djh"
    home_scripts = os.path.abspath('../')

    shortcuts_folder = data.pathExt()

    bash_rc = """
# Magic dcore tag: %s.
export PYTHONPATH=$PYTHONPATH:%s
export PATH=$PATH:%s
    """ % (tag, home_scripts, shortcuts_folder)

    bash_rc = bash_rc.replace('__home__', os.path.expanduser('~'))

    fname = os.path.expanduser('~/.profile')
    file = open(fname, 'r').read()
    if not tag in file:
            file = bash_rc + '\n\n' + file
            open(fname, 'w').write(file)

    os.system('source ~/.profile')

def setupShortcuts():
    data.createAllDirs()
    system_setup.create_python_scripts_shortcuts.do()

if __name__ == '__main__':
    setupShortcutsBootstrap()
    setupShortcuts()

