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

    tag = data.tagShortcutsForDeletion()
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

    """
    :::issue here reported on cmd
    print('sourcing')
    cmd = 'source %s' % fname
    print(cmd)
    os.system(cmd)
    """

def setupShortcuts():
    data.createAllDirs()
    create_python_scripts_shortcuts.do()

def delOld():
    folder = data.pathExt()

    tag = data.tagShortcutsForDeletion()
    files = os.listdir(folder)
    for file in files:
        with open(file, 'r') as fh:
            content = fh.read()

        if tag in content:
            print('Deleting %s.' % file)
            os.remove(file)

if __name__ == '__main__':
    delOld()
    setupShortcutsBootstrap()
    setupShortcuts()

