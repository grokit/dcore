"""
Define where data is.
"""

import sys
import os

import platform

def createAllDirs():
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

def dcoreRoot():
    return os.path.abspath(os.path.split(__file__)[0])

def dcoreData(tolerateNonExist = False):

    usualPath = os.path.abspath(os.path.expanduser('~/sync/dcore_data'))

    if platform.system() == "Windows":
        # All potential places where dcoreData can be.
        dirs = []
        dirs.append(r'c:\david\dcore_home')
        dirs.append(usualPath)
        dirs = [p for p in dirs if os.path.isdir(p)]
        assert len(dirs) <= 1
        if tolerateNonExist:
            assert len(dirs) == 0
            return usualPath
        else:
            assert len(dirs) == 1
            return dirs[0]
    else:
        return usualPath

def pathExt():
	return os.path.normpath(os.path.join(dcoreData(), './path_ext'))
    
if __name__ == '__main__':
    createAllDirs()
    print('data: ' + dcoreData())
    print('root: ' + dcoreRoot())
    print('ext:  ' + pathExt())
