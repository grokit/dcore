#!/usr/bin/python3.4
"""
Creates shell-accessible command line shortcuts for applications that have a meta-tag.

# TODO

- Merge with install.py?
"""

import os
import re
import sys

import dcore.search_files as fsearch
import dcore.data as data

shell_meta_search = '_meta_shell_command'
_meta_shell_command = 'generate_shortcuts'


def isOK(file):
    if file.find('__') != -1: return False
    dirname = os.path.dirname(file)
    dirs = dirname.split('/')
    for d in dirs:
        if d == 'deprecated':
            return False
    return True


def getRoots():
    return [data.dcoreRoot(), data.dcoreExtRoot()]


def findPyFiles():
    scriptFolders = getRoots()

    P = []
    for scriptFolder in scriptFolders:
        pyfiles = fsearch.getAllFilesRecursively('*.py', scriptFolder)
        P += [pyfile for pyfile in pyfiles if isOK(pyfile)]

    return P


def delCurrentShortcuts():
    "Delete all files that have special marker inside output directory."
    scriptsOutputFolder = data.pathExt()

    tag = data.tagShortcutsForDeletion()
    for f in os.listdir(scriptsOutputFolder):
        f = os.path.join(scriptsOutputFolder, f)
        with open(f, 'r') as fh:
            fdata = fh.read()
        if tag in fdata:
            print('Deleting script shortcut: %s.' % f)
            os.remove(f)


def getAutogenFileTemplate():

    file_template = r"""
# Automatically created by '%s', do not modify.
# Tag for easy deletion: %s

__custom__ """ % (os.path.normpath(__file__), data.tagShortcutsForDeletion())

    return file_template


def getMetadataFromPyFiles(pyfiles):
    """
    meta: (python file, shell command, special flags)

    :::meta[0, 1 or 2] is confusing. Just create a class with names entities.
    """

    meta = []
    for file in pyfiles:
        fh = open(file, 'r')
        lines = fh.readlines()
        fh.close()

        for line in lines:
            m = re.search(shell_meta_search + ".*=.*'(.*)'", line)
            if m is not None:
                command = m.groups(0)[0]
                if len(command.split(' ')) > 1:
                    laucher = command.split(' ')[0]
                    args = " ".join(command.split(' ')[1:])
                else:
                    laucher = command
                    args = ''
                meta.append((file, laucher, args))

    return meta


def createShortcuts(lMeta):

    file_template = getAutogenFileTemplate()
    scriptsOutputFolder = data.pathExt()

    for meta in lMeta:
        fileContent = file_template
        fileContent = fileContent.replace('__py_file__', meta[0])
        fileContent = fileContent.replace('__opt_cmd__', meta[2])

        fileContent = fileContent.replace('__custom__',
                                          'python3 %s $*' % meta[0])

        fileOut = scriptsOutputFolder + "/" + meta[1]
        fileOut = os.path.normpath(fileOut)

        print((meta, fileOut))

        fh = open(fileOut, 'w')
        fh.write(fileContent)
        fh.close()
        os.system('chmod +x %s' % fileOut)


def do():
    pyFiles = findPyFiles()
    delCurrentShortcuts()
    meta = getMetadataFromPyFiles(pyFiles)
    createShortcuts(meta)


if __name__ == "__main__":
    do()
