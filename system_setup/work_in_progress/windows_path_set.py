r"""
Set environment variables permanently on Windows.

Note: must be administrator.
"""

import os
import sys

import dcore.system_description as private_data

SYS_PATH_ADD_IF_NOT_PRESENT = [
r'c:\python32',
r'c:\python33',
r'c:\python27',
r'c:\david\sync\Dropbox\scripts\path_ext',
r'C:\Users\%s\Desktop\Dropbox\scripts\path_ext' % private_data.muname]

SYS_ENV_VARS_ADD_OR_CLOBBER = {
'PYTHONPATH': r'c:\david\sync\Dropbox\scripts;C:\Users\%s\Desktop\Dropbox\scripts' %s private_data.muname,
'DTG_ROOT': r'c:\david\sync',
'DESKTOP': os.path.join(os.environ['userprofile'], 'desktop')
}

def listRemoveDuplicates(lst):
    return list(set(list(lst)))

def getSysPathAsList():
    return listRemoveDuplicates( os.environ['path'].split(';') )

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
    
    
    
