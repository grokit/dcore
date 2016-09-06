
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
    pyPublic = data.dcoreRoot()
    pyfiles = fsearch.getAllFilesRecursively('*.py', pyPublic)

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
                of.append((pfile,stag))
                break

    return of 

if __name__ == '__main__':
    args = getArgs()

    editor = 'vim'

    efiles = findExecutableScripts()

    filename = []
    for f, tag in efiles:
        if tag == args.shortcut_to_edit:
            filename.append(f)

    assert len(filename) == 1
    filename = filename[0]
    cmd = 'vim %s' % filename
    print(cmd)
    os.system(cmd)

