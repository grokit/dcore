
import sys
import os
import argparse
import platform
import dataclasses

import dcore.data as data
import dcore.utils as dutils
import dcore.utils as dutils

PATH_EXT_FOLDER = data.pathExt()
CACHE_FILE = os.path.join(data.dcoreData(), 'dr.py.cache')
CACHE_FILE_DELETED = CACHE_FILE + ".deleted"


@dataclasses.dataclass
class DirShortcut:
    path: str
    # shortcut for this directory, without the cd
    # e.g. 01, then will be accessible with . cd01
    shortcut: str = None

def write_to_disk(dirs_shortcuts):
    fh = open(CACHE_FILE, 'w')
    for ds in dirs_shortcuts:
        if ds.shortcut is None:
            fh.write(f'{ds.path}')
        else:
            fh.write(f'{ds.shortcut},{ds.path}')
        fh.write("\n")
    fh.close()

def __create_shortcut(new_file, dir):
    tag = 'Auto del tag: ' + data.tagShortcutsForDeletionForDr()
    if platform.system() == 'Windows':
        new_file += '.bat'
    with open(new_file, 'w') as fh:
        if platform.system() == 'Windows':
            fh.write('Rem %s\ncd /d "%s"' % (tag, dir))
        else:
            fh.write('# %s\ncd "%s"' % (tag, dir))

def __file_lines_to_typed_class(dirs):
    last = None
    to_create = []
    for i, dir in enumerate(dirs):
        assert ',' in dir
        shortcut, unpacked_dir = dir.split(',')
        shortcut = r'%s' % shortcut
        to_create.append((unpacked_dir, shortcut))
        last = dir

    # todo:::a1 re-implement
    # cdl always point to last folder
    #to_create.append((last, 'l'))

    # as type
    out = []
    for directory, shortcut in to_create:
        out.append(DirShortcut(path=directory, shortcut=shortcut))
    return out

def __create_shortcuts_sane(dir_shortcuts):
    for ds in dir_shortcuts:
        new_file = os.path.join(PATH_EXT_FOLDER, f'cd{ds.shortcut}')
        __create_shortcut(new_file, ds.path)
        #print(f'create shortcut for as file: {new_file} with inner go to dir: {ds.path}')

##########################################################################
# PUBLIC
##########################################################################

def dr_nums_dupl_and_seen(dirs_typed):
    seen_path = set()
    out = []
    for dd in dirs_typed:
        if dd.path not in seen_path:
            seen_path.add(dd.path)
            out.append(dd)
    out = out[0:9]
    return out

def remember_dir_typed(dir_shortcut):
    dirs_typed = __file_lines_to_typed_class(get_file_content_as_list())

    # at this point:
    # ds.shortcut: shortcut name e.g. 01
    # ds.path: the file the shortcut is for

    dirs_typed.reverse()

    numbers = []
    named = []
    seen_names = set()
    for ds in dirs_typed:
        if ds.shortcut.isdigit():
            numbers.append(ds)
        else:
            if ds.shortcut not in seen_names:
                named.append(ds)
                seen_names.add(ds.shortcut)

    if dir_shortcut.shortcut is None:
        numbers = [dir_shortcut] + numbers
    else:
        named.append(dir_shortcut)

    numbers = dr_nums_dupl_and_seen(numbers)
    i = 1
    for nn in numbers:
        nn.shortcut = r'%01d' % i
        i += 1
    numbers.reverse()

    dirs_typed = named + numbers

    write_to_disk(dirs_typed)

    # write shortcuts
    dutils.delCurrentShortcuts(data.tagShortcutsForDeletionForDr())
    __create_shortcuts_sane(dirs_typed)


def remember_dir(directory):
    return remember_dir_typed(DirShortcut(path=directory, shortcut=None))


def get_file_content_as_list():
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
    if not os.path.isdir(PATH_EXT_FOLDER):
        raise Exception(PATH_EXT_FOLDER)

    data = []
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as fh:
            data = fh.read()
            fh.close()
        data = data.splitlines()
    return data


