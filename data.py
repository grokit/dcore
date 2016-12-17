"""
Define where data is.

BE CAREFUL WITH dcore IMPORTS IN THAT FILE. It is used during install, anything that depends
on path being set properly will fail the install.
"""

import sys
import os
import platform

def tagShortcutsForDeletion():
    return "0jb02xhs83hayd9fugb7wu2as3q419ki"

def dcoreRoot():
    """
    Root of where all scripts are: where this file is.
    """
    return os.path.abspath(os.path.split(__file__)[0])

def dcoreTempData():
    return os.path.abspath(os.path.expanduser('~/sync/dcore_data_temp'))

def dcoreData():
    return os.path.abspath(os.path.expanduser('~/sync/dcore_data'))

def pathExt():
    """
    Where we put generated shortcuts that are in path.
    """
    return os.path.normpath(os.path.join(dcoreData(), './path_ext'))

def createAllDirsIfNotExist():
    """
    Run once on install, creates directories for scripts if does not exist already.
    """
    dirs = []
    dirs.append(dcoreData())
    dirs.append(pathExt())

    for dData in dirs:
        if not os.path.isdir(dData):
            print('Creating %s.' % dData)
            os.makedirs(dData)

if __name__ == '__main__':
    createAllDirs()
    print('data: ' + dcoreData())
    print('root: ' + dcoreRoot())
    print('ext:  ' + pathExt())
