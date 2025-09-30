"""

# FEATURES

- record how often shortcuts are used

================================================================================
# OLD
================================================================================

# BUGS

- Same key can be there multiple times ... forbid at entry.
- Need to cleanup on refresh do that removed shortcuts gets removes (use tag like other apps use).

# Documentation

`dr -r` will permanently remember current directory.
`dr` lists all directory remembered and their tags.

Each directory gets a tag (by default 00...99), to go to that directory simply type:
. cd<tag>

e.g:
cd01
cd03

Note that in Windows you do not need the `. ` prefix, simply type cd01, cd02.

# TODO

- . drl <-- go to latest remembered?

- dr: should keep remembered dirs in s small stack instead of alphabetical
    . cdl1, cdl2: goes to two remembered dir ago, even if not named --> makes dr -r more useful as a stack

- Also support remembering and opening files:
    . cd<folder-tag>
    . op<file-tag>
    ^^ or maybe better to have a separate utility since the `. x` syntax is not necessary to open files.

- Instead of sorting, just keep things in order added.
    1 list of tagged, one for just number `. cd0` should always go to last folder

- Auto-tag:
    - dr -r <tag>: remember current dir.
    dr -r NAME --> should set name shortcut auto

- Also be able to remember files:
    - dr [filename] <tag>: remember file. After this, dr -e [file or tag] staight-up open in vim.
    ^^ then retire the `fopen` utility.

don't delete, write to 'deleted' file.
    dr -d --> open deleted file

# Misc / Alternative

Other silimar Project: http://linuxgazette.net/109/marinov.html

- CDPATH, try application `autojump`

# BUGS
"""

_meta_shell_command = 'dr'

import sys
import os
import argparse
import platform

import dcore.apps.quickdir.lib as quickdir_lib



def printStoredDirs():
    data = quickdir_lib.get_file_content()

    i = 0
    for file in data:
        print("%02d: %s" % (i, file))
        i += 1


def do():

    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--remember', action="store_true")
    parser.add_argument('-p', '--print', action="store_true")
    parser.add_argument('-e', '--edit', action="store_true")

    args = parser.parse_args()
    cacheFile = quickdir_lib.cacheFile
    print('Using cache file: %s.' % cacheFile)

    if not os.path.isfile(cacheFile):
        fh = open(cacheFile, 'w')
        fh.write('')
        fh.close()

    if args.print:
        printStoredDirs()
        exit(0)

    if args.edit:
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

    printStoredDirs()


if __name__ == '__main__':
    do()
