"""
# BUGS

- Same key can be there multiple times ... forbid at entry.

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

- . drl <-- go to latest remembered ... same as .cd0?

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

# Misc

Other silimar Project: http://linuxgazette.net/109/marinov.html

# BUGS

- Old shortcuts not deleted.

"""

_meta_shell_command = 'dr'

import sys
import os
import argparse
import platform

import dcore.data as data

path_ext_folder = data.pathExt()
cacheFile = os.path.join(data.dcoreData(),
                         '%s.cache' % os.path.split(__file__)[1])
cacheFilePerimated = cacheFile + ".deleted"
tempBatch = cacheFile + '.temp.bat'


def rememberDirs():

    dirs = getFileContent()
    # append at END to have stable numbering
    dirs += [os.getcwd()]

    bad = [
        d for d in dirs if not os.path.isdir(d)
        and not (len(d.split(',')) == 2 and os.path.isdir(d.split(',')[1]))
    ]

    if len(bad) > 0:
        print('Removing non-existent directories: %s.' % bad)
        with open(cacheFilePerimated, 'a') as fh:
            fh.write("\n".join(bad))
            fh.write("\n")

    dirs = [d for d in dirs if d not in bad]

    setFileContent(dirs)

    # need to read again because might be different if there are duplicates
    dirs = getFileContent()

    # create shortcut files
    if os.path.isdir(path_ext_folder):
        i = 0
        for dir in dirs:

            shortcut = ''
            if ',' in dir:
                shortcut, dir = dir.split(',')

            new_file = os.path.join(path_ext_folder, r'cd%02d' % i)
            if platform.system() == 'Windows':
                new_file += '.bat'
            fh = open(new_file, 'w')
            if platform.system() == 'Windows':
                fh.write('cd /d "%s"' % dir)
            else:
                fh.write('cd "%s"' % dir)

            if shortcut != '':
                new_file = os.path.join(path_ext_folder, r'cd%s' % shortcut)
                if platform.system() == 'Windows':
                    new_file += '.bat'
                fh = open(new_file, 'w')
                if platform.system() == 'Windows':
                    fh.write('cd /d "%s"' % dir)
                else:
                    fh.write('cd "%s"' % dir)

            fh.close()
            i += 1
    else:
        raise Exception(path_ext_folder)


def getFileContent():
    """
    # File Format
    
        [tag,]<file>
        ...
        [tag,]<file>
    
    e.g:
    
        jl,/journal
        /etc
    
    '/etc' is a non-tag shortcut, will be accessible with a number.
    '/journal' will be accessible with a number OR cdjl.
    """

    fh = open(cacheFile, 'r')
    data = fh.read()
    fh.close()

    data = data.splitlines()

    return data


def eliminateDup(lst: list):

    # Reverse so that eliminates EARLIER entry.
    # This does not preserve numbering (bad), but
    # it does make sure new dir gets back on top of
    # stack.
    lst.reverse()

    st = set()
    out = []
    for l in lst:
        if l not in st:
            out.append(l)
        st.add(l)

    out.reverse()
    return out


def setFileContent(fileList):
    fileList = eliminateDup(fileList)

    fh = open(cacheFile, 'w')

    for file in fileList:
        fh.write(file)
        fh.write("\n")
    fh.close()


def printStoredDirs():
    data = getFileContent()

    i = 0
    for file in data:
        print("%02d: %s" % (i, file))
        i += 1


def do():

    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--remember', action="store_true")
    parser.add_argument('-p', '--print', action="store_true")
    parser.add_argument('-e', '--edit', action="store_true")
    parser.add_argument('-g', '--goto_clip', type=int)

    args = parser.parse_args()
    #print(args)
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
        rememberDirs()
        exit(0)

    if args.remember:
        rememberDirs()
        printStoredDirs()
        exit(0)

    if args.goto_clip != None:
        """
        BUG: this does not work (anymore?).
        """
        filec = getFileContent()
        dir = filec[args.goto_clip]

        try:
            from tkinter import Tk
        except:
            pass

        if Tk is not None:
            r = Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(dir)
            r.destroy()
        else:
            print('Tk not available, clipboard functions will not work.')

        print("'%s' now in clipboard" % dir)
        exit(0)

    printStoredDirs()


if __name__ == '__main__':
    do()
