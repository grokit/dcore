"""
Define where data is.

Makes sure that are folders exist, create a hook for applications to know where to fetch data from.
Also a good place to document hierarchy.

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

def dcoreBackupsSysSettings():
    return os.path.abspath(os.path.expanduser('~/sync/archive/backups'))

def pathExt():
    """
    Where we put generated shortcuts that are in path.
    """
    return os.path.normpath(os.path.join(dcoreData(), './path_ext'))

def createDirIfNotExist(dData):
    if not os.path.isdir(dData):
        os.makedirs(dData)

def getDirs():
    dirs = []
    dirs.append(dcoreData())
    dirs.append(dcoreTempData())
    dirs.append(pathExt())
    dirs.append(dcoreBackupsSysSettings())
    return dirs

def createAllDirsIfNotExist():
    """
    Run once on install, creates directories for scripts if does not exist already.
    """

    for dData in getDirs():
        createDirIfNotExist(dData)

