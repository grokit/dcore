r"""
Set environment variables permanently on Windows.

Note: must be administrator.
"""

import os
import sys
import pathlib

import dcore.data as data

SYS_PATH_ADD_IF_NOT_PRESENT = [
r'c:\python32',
r'c:\python33',
r'c:\python34',
r'c:\python35',
r'c:\python36',
]

def getRootPath():
    # dcore root supposed to be one dir up from here.
    # Would be better to rely on a tag file in the root directory.
    filepath = os.path.realpath(__file__)
    return pathlib.Path(filepath).parents[2].as_posix()

def getShortcutsPath():
	return os.path.join(getRootPath(), './dcore/path_ext')

def listRemoveDuplicates(lst):
    # Maintain relative order in the original list.
    D = {}
    for i, l in enumerate(lst):
        D[l] = i
    print(D)
    lst = [l for l in list(set(list(lst))) if len(l) > 0]
    lst.sort(key= lambda x: D[x])
    return lst

def getSysPathAsList():
    raise Exception("Do not use this as this gets the merge system and user path.")
    return os.environ['path'].split(';')

def setPermanentEnvironmentVariable(name, var):
    print("Setting: '%s' as '%s'." % (name,var))
    
    if len(var) >= 1024:
        raise Exception("Length(path): %i. Not setting since windows cannot handle > 1024 len on command-line, doing so would corrupt the path." % len(var))
    
    # /M if want to change sys. env.var
    cmd = "setx %s \"%s\"" % (name, var)
    print(cmd)
    os.system(cmd)

def isValidPath(p):
    if p in ['PLACEHOLDER_COMPILERS']:
        return True
    return os.path.isdir(p)

def do():
    
    # Completely whacks user's path variable. Know what you are doing before running this :).
    
    sPath = []
    
    sPath.append(os.path.join(data.pathExt()))
    
    # Special folders for windows env.
    sPath.append(r'C:\Program Files\Git\cmd')
    sPath.append(r'c:\Windows\SysWOW64\WindowsPowerShell\v1.0')
    sPath.append(os.path.join(getRootPath(), './../scripts/path_ext'))
    
    sPath.append(getRootPath())
    for p in SYS_PATH_ADD_IF_NOT_PRESENT:
        sPath.append(p)
    
    sPath = [os.path.normpath(p) for p in sPath]
    sPath = listRemoveDuplicates(sPath)
    
    for p in [p for p in sPath if not isValidPath(p)]:
        print("Warning, '%s' is not a valid path and will be removed." % p)
        
    sPath = [p for p in sPath if isValidPath(p)]
    sPath = ";".join(sPath)
    
    #print(sPath)
    setPermanentEnvironmentVariable('PATH', sPath)
    
    sysEnvVarsAddOrClobber = {
        'PYTHONPATH': getRootPath() + ';' + r'c:\david\scripts',
        'DESKTOP': os.path.join(os.environ['userprofile'], 'desktop')
    }
    
    for k, v in sysEnvVarsAddOrClobber.items():
        setPermanentEnvironmentVariable(k, v)   
       
def fix():
    sPath = r';;'
    sPath = sPath.split(';')
    sPath = listRemoveDuplicates(sPath)
    
    for p in [p for p in sPath if not isValidPath(p)]:
        print("Warning, '%s' is not a valid path and will be removed." % p)
        
    sPath = [p for p in sPath if isValidPath(p)]
    sPath = ";".join(sPath)
    print(sPath)

if __name__ == "__main__":
    do()
    
    
