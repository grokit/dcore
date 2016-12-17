#!/usr/bin/python3

"""
One-run install of `dcore`.
"""

import sys
import os
import platform

def setupShortcutsBootstrap():
    """
    We put all shortcuts in dcore-owned directory and add it to executable PATH loaded by shell.
    """

    # This import should be fine as it does not depend on path.
    import data

    tag = data.tagShortcutsForDeletion()
    home_scripts = os.path.abspath('../')

    shortcuts_folder = data.pathExt()

    bash_rc = """
# Magic dcore tag: %s_BEGIN.
export PYTHONPATH=$PYTHONPATH:%s
export PATH=$PATH:%s
# %s_END
    """ % (tag, home_scripts, shortcuts_folder, tag)

    bash_rc = bash_rc.replace('__home__', os.path.expanduser('~'))

    fname = os.path.expanduser('~/.profile')
    file = open(fname, 'r').read()
    if not tag in file:
        file = bash_rc + '\n\n' + file
        open(fname, 'w').write(file)
    else:
        print('Warning: skipping writing new `%s` since it looks like tag is already present.' % fname)

    cmd = 'source %s' % fname
    print(cmd)
    os.system(cmd)

def setupShortcuts():
    create_python_scripts_shortcuts.do()

def delOld():
    folder = data.pathExt()

    tag = data.tagShortcutsForDeletion()
    files = [os.path.join(folder, f) for f in os.listdir(folder)]
    for file in files:
        with open(file, 'r') as fh:
            content = fh.read()

        if tag in content:
            print('Deleting %s.' % file)
            os.remove(file)

def tryImports():
    try:
        import dcore.data as data
        import dcore.create_python_scripts_shortcuts as create_python_scripts_shortcuts
        global data
        global create_python_scripts_shortcuts
        return True
    except ImportError as e:
        return False

if __name__ == '__main__':

    if not tryImports():
        print('Not bootstrapped, ')
        print('Attempting to bootstrap. You may need to restart your terminal for changes to take effect.')
        setupShortcutsBootstrap()
        exit(0)

    data.createAllDirsIfNotExist()
    delOld()
    setupShortcuts()

