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
import dataclasses

import dcore.data as data
import dcore.utils as dutils
import dcore.utils as dutils

PATH_EXT_FOLDER = data.pathExt()
cacheFile = os.path.join(data.dcoreData(), 'dr.py.cache')
cacheFileDeleted = cacheFile + ".deleted"

@dataclasses.dataclass
class DirShortcut:
    path: str
    shortcut: str = None

def __createSortcut(new_file, dir):
    tag = 'Auto del tag: ' + data.tagShortcutsForDeletionForDr()
    if platform.system() == 'Windows':
        new_file += '.bat'
    with open(new_file, 'w') as fh:
        if platform.system() == 'Windows':
            fh.write('Rem %s\ncd /d "%s"' % (tag, dir))
        else:
            fh.write('# %s\ncd "%s"' % (tag, dir))

def __create_shortcuts_insane():
    if not os.path.isdir(PATH_EXT_FOLDER):
        raise Exception(PATH_EXT_FOLDER)

    dirs = get_file_content()

    last = None
    to_create = []
    for i, dir in enumerate(dirs):

        # named labels: cddev, cdgame, ...
        if ',' in dir:
            shortcut, unpacked_dir = dir.split(',')
            # cdl == cd last, it has a special meaning
            assert shortcut != 'l'
            #new_file = os.path.join(PATH_EXT_FOLDER, r'cd%s' % shortcut)
            shortcut = r'cd%s' % shortcut
            to_create.append((unpacked_dir, shortcut))
            # also create a numerical label
            #new_file = os.path.join(PATH_EXT_FOLDER, r'cd%02d' % i)
            shortcut = r'cd%02d' % i
            to_create.append((unpacked_dir, shortcut))
            last = unpacked_dir
        else:
            # numerical labels: cd01, cd02, ...
            #new_file = os.path.join(PATH_EXT_FOLDER, r'cd%02d' % i)
            shortcut = r'cd%02d' % i
            to_create.append((dir, shortcut))
            last = dir

    # cdl always point to last folder
    to_create.append((last, 'cdl'))


    out = []
    for directory, shortcut in to_create:
        out.append(DirShortcut(path=directory,shortcut=shortcut))

    __create_shortcuts_sane(out)

def __create_shortcuts_sane(dir_shortcuts):
    for ds in dir_shortcuts:
        new_file = os.path.join(PATH_EXT_FOLDER, ds.shortcut)
        __createSortcut(new_file, ds.path)

def remember_dir_typed(dir_shortcut):
    """
    This is not ideal since it forces remembering only curr dir,
    have parameter instead.
    """

    dirs = get_file_content()
    # append at END to have stable numbering
    if dir_shortcut.shortcut is None:
        dirs += [dir_shortcut.path]
    else:
        dirs += [f'{dir_shortcut.shortcut},{dir_shortcut.path}']

    bad = set([
        d for d in dirs if not os.path.isdir(d)
        and not (len(d.split(',')) == 2 and os.path.isdir(d.split(',')[1]))
    ])

    if len(bad) > 0:
        # do not print, it can create issues when in vi plugin
        #print('Removing non-existent directories: %s.' % bad)
        with open(cacheFileDeleted, 'a') as fh:
            fh.write("\n".join(bad))
            fh.write("\n")

    dutils.delCurrentShortcuts(data.tagShortcutsForDeletionForDr())

    dirs = [d for d in dirs if d not in bad]

    setFileContent(dirs)
    __create_shortcuts_insane()


def remember_dir(directory):
    return remember_dir_typed(DirShortcut(path=directory,shortcut=None))

def get_file_content():
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
    with open(cacheFile, 'r') as fh:
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

