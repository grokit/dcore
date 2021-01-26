"""
Opens a Python script from its shortcut in the `dcore` system.

Usage:

    edits <script-shortcut>

# TODO

- Replace with `editw`: edit the file that `which` points to.
which python3 | xargs vi -> editw python3

- OR replace with dcore where you can do many things
    dcore -l : list all apps
    dcore -e <app>: edit app
"""

import dcore.search_files as fsearch
import dcore.create_python_scripts_shortcuts as scripts_info
import dcore.data as data

import argparse
import os

_meta_shell_command = 'edits'


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('shortcut_to_edit')
    args = parser.parse_args()
    return args


def findExecutableScripts():
    pyfiles = fsearch.getAllFilesRecursively('*.py', data.dcoreRoot())
    pyfiles += fsearch.getAllFilesRecursively('*.py', data.dcoreExtRoot())

    tag = scripts_info.shell_meta_search

    of = []
    for pfile in pyfiles:
        lines = open(pfile).readlines()

        for l in lines:
            if tag in l:
                stag = l.split('=')[1].strip()
                if len(stag) > 1: stag = stag.split(' ')[0]
                stag = stag.strip('"')
                stag = stag.strip("'")
                of.append((pfile, stag))
                break

    return of


if __name__ == '__main__':
    args = getArgs()

    editor = 'vi'

    efiles = findExecutableScripts()

    filename = []
    for f, tag in efiles:
        if tag == args.shortcut_to_edit:
            filename.append(f)

    if len(filename) != 1:
        print(filename)
        assert len(filename) == 1

    filename = filename[0]
    cmd = 'vi %s' % filename
    print(cmd)
    os.system(cmd)
