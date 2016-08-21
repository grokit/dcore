"""
Define where data is.
"""

import sys
import os
import platform

def tagShortcutsForDeletion():
    #:::replace with truly random.
    return "9sdj09dj9sa8j9d8sjs9djdsa9jas9d8jsad9jsda98jsad89sjda89sjda9"

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

def createAllDirs():
    """
    Run once on install, creates directories for scripts if does not exist already.
    :::rename: ifNotExist
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
