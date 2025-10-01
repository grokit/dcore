"""
Create a shortcut for a directory:

    /a/dir dr -r

... then at a later time:

    . cd01

    -> goes to /a/dir

# FEATURES / ideas

- record how often shortcuts are used
- be able to name a dir without having to edit file (meh)

# misc

- Linux: . cd01
- Windows: you do not need the `. ` prefix, simply type cd01, cd02.
- other silimar projects
    - http://linuxgazette.net/109/marinov.html
    - CDPATH, try application `autojump`

# BUGS

- Same key / shortcut can be there multiple times ... forbid at entry.
- Cut down to 10 autonum -- not sure the point to have 100s
"""

import dcore.apps.quickdir.lib as quickdir_lib
import platform
import argparse
import os
import sys
_meta_shell_command = 'dr'


def printStoredDirs():
    data = quickdir_lib.get_file_content_as_list()
    for dd in data:
        print(dd)


def do():

    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--remember', action="store_true")
    parser.add_argument('-e', '--edit', action="store_true")

    args = parser.parse_args()

    if args.edit:
        cacheFile = quickdir_lib.CACHE_FILE
        if platform.system().lower() == 'windows':
            os.system('np ' + cacheFile)
        else:
            os.system('vim ' + cacheFile)
        quickdir_lib.remember_dir(os.getcwd())
        exit(0)

    if args.remember:
        quickdir_lib.remember_dir(os.getcwd())
        if False:
            printStoredDirs()
        exit(0)

    # default ...
    printStoredDirs()


if __name__ == '__main__':
    do()
