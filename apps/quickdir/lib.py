"""
want to create a shortcut for a directory:

    /a/dir dr -r <name>

then at a later time:

    . cd<name> 

    this goes to that dir
"""

import sys
import os
import argparse
import platform

import dcore.data as data
import dcore.utils as dutils
import dcore.utils as dutils

path_ext_folder = data.pathExt()
cacheFile = os.path.join(data.dcoreData(), 'dr.py.cache')
cacheFileDeleted = cacheFile + ".deleted"


def rememberDirs():
    """
    This is not ideal since it forces remembering only curr dir,
    have parameter instead.
    """

    dirs = getFileContent()
    # append at END to have stable numbering
    dirs += [os.getcwd()]

    bad = [
        d for d in dirs if not os.path.isdir(d)
        and not (len(d.split(',')) == 2 and os.path.isdir(d.split(',')[1]))
    ]

    if len(bad) > 0:
        print('Removing non-existent directories: %s.' % bad)
        with open(cacheFileDeleted, 'a') as fh:
            fh.write("\n".join(bad))
            fh.write("\n")

    dutils.delCurrentShortcuts(data.tagShortcutsForDeletionForDr())

    dirs = [d for d in dirs if d not in bad]

    setFileContent(dirs)

    # need to read again because might be different if there are duplicates
    dirs = getFileContent()

    def createSortcut(new_file, dir):
        tag = 'Auto del tag: ' + data.tagShortcutsForDeletionForDr()
        if platform.system() == 'Windows':
            new_file += '.bat'
        with open(new_file, 'w') as fh:
            if platform.system() == 'Windows':
                fh.write('Rem %s\ncd /d "%s"' % (tag, dir))
            else:
                fh.write('# %s\ncd "%s"' % (tag, dir))

    # create shortcut files
    if os.path.isdir(path_ext_folder):
        for i, dir in enumerate(dirs):

            # named labels: cddev, cdgame, ...
            if ',' in dir:
                shortcut, unpacked_dir = dir.split(',')
                # cdl == cd last, it has a special meaning
                assert shortcut != 'l'
                new_file = os.path.join(path_ext_folder, r'cd%s' % shortcut)
                createSortcut(new_file, unpacked_dir)
                # also create a numerical label
                new_file = os.path.join(path_ext_folder, r'cd%02d' % i)
                createSortcut(new_file, unpacked_dir)
            else:
                # numerical labels: cd01, cd02, ...
                new_file = os.path.join(path_ext_folder, r'cd%02d' % i)
                createSortcut(new_file, dir)

        # cdl always point to last folder
        new_file = os.path.join(path_ext_folder, r'cdl')
        createSortcut(new_file, dir)

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

def create_shortcut(directory, shortcut_name):
    pass
