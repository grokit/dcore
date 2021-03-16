"""
Define folder locations and small pieces of data.

Makes sure that are folders exist, create a hook for applications to know where to fetch data from.
Also a good place to document hierarchy.

BE CAREFUL WITH dcore IMPORTS IN THAT FILE. It is used during install, anything that depends
on path being set properly (in this file) will fail the install.
"""

import sys
import os
import platform


def getBashrcOrEquivalent():
    """
    https://apple.stackexchange.com/questions/51036/what-is-the-difference-between-bash-profile-and-bashrc
    """
    if platform.system() in ["macosx", "Darwin"]:
        return os.path.expanduser('~/.bash_profile')
    else:
        return os.path.expanduser('~/.bashrc')


def tagShortcutsForDeletion():
    return "0jb02xhs83hayd9fugb7wu2as3q419ki"


def dcoreRoot():
    """
    Root of where all scripts are: where this file is.
    """
    return os.path.abspath(os.path.split(__file__)[0])


def dcoreExtRoot():
    """
    If exist, return extention folder for user's private scripts.
    """
    return os.path.join(os.path.split(dcoreRoot())[0], 'dcore_ext')


def dcoreTempData():
    return os.path.abspath(os.path.expanduser('~/sync/dcore_data_temp'))


def logsdir():
    return dcoreTempData() + '/logs'


def dcoreData():
    return os.path.abspath(os.path.expanduser('~/sync/dcore_data'))


def dcoreBackupEnv():
    """
    Consider just putting in `backups/rolling/env` and zip + encrypt since
    could contain pws if typed by mistake in shell.
    """
    return os.path.expanduser('~/sync/archive/backups/rolling/env/auto')


def backup_phone_dir():
    return os.path.expanduser('~/sync/archive/backups/rolling/phone/auto')

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
    return dirs


def createAllDirsIfNotExist():
    """
    Run once on install, creates directories for scripts if does not exist already.
    """

    for dData in getDirs():
        print('Creating %s if not exist.' % dData)
        createDirIfNotExist(dData)
