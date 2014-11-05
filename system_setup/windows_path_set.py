r"""
Set environment variables permanently on Windows.

Note: must be administrator.
"""

import os
import sys
import pathlib

SYS_PATH_ADD_IF_NOT_PRESENT = [
r'c:\python32',
r'c:\python33',
r'c:\python27']

def getRootPath():
    filepath = os.path.realpath(__file__)
    return pathlib.Path(filepath).parents[2].as_posix()

def getShortcutsPath():
	return os.path.join(getRootPath(), './dcore/path_ext')

SYS_ENV_VARS_ADD_OR_CLOBBER = {
'PYTHONPATH': getRootPath(),
'DESKTOP': os.path.join(os.environ['userprofile'], 'desktop')
}

def listRemoveDuplicates(lst):
    return list(set(list(lst)))

def getSysPathAsList():
    listPath = listRemoveDuplicates( os.environ['path'].split(';') )
    listPath.append( getShortcutsPath() )
    return listRemoveDuplicates( listPath )

def setPermanentEnvironmentVariable(name, var):
    
    cmd = "setx -m %s \"%s\"" % (name, var)
    print(cmd)
    os.system(cmd)
    
if __name__ == "__main__":
    
    # SYS_PATH_ADD_IF_NOT_PRESENT
    
    sPath = getSysPathAsList()
    
    for p in SYS_PATH_ADD_IF_NOT_PRESENT:
        sPath.append(p)
    
    sPath = listRemoveDuplicates(sPath)
    
    sPath = ";".join(sPath)
    
    setPermanentEnvironmentVariable('PATH', sPath)
    
    # SYS_ENV_VARS_ADD_OR_CLOBBER
    
    for k, v in SYS_ENV_VARS_ADD_OR_CLOBBER.items():
        setPermanentEnvironmentVariable(k, v)
    
    
    
