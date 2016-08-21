"""
Allows to load env parameters (incuding passwords, etc) from private files outside of repository.

File is due for house-cleaning and renaming.
"""

import os
import json
import pathlib
import platform

import dcore.data as data

def getPrivateDataFilename():
    return os.path.join(data.dcoreData(), "private_file_v2")

def __loadPrivateFile():

    if os.path.isfile(getPrivateDataFilename()):
        fh = open(getPrivateDataFilename(), 'r')
        jr = fh.read()
        fh.close()
    else:
        print('Warning: cannot find private file %s.' % getPrivateDataFilename())
        jr = "{}"

    return json.loads(jr)

def __expandEnvVars(D):
    r"""
    %userprofile%: c:\users\userid
    $var: an_env_variable_expanded
    """
    return {k:os.path.expandvars(v) for (k, v) in D.items()}
    
# :::cleanup BAN THIS. This is way to magicky.
# This will add all the variables declared in the JSON file as local variables.
# This way, system_description.variable is accessible after importing the module.
# Could relegate this as private.py and ONLY be used for passwords and the such ... but need to explain in exception when not found that this is data the user needs to set.
jd = __loadPrivateFile()
localsDir = locals()
if 'variables' in jd.keys():
    for k, v in jd['variables'].items():
        localsDir[k] = v

if __name__ == '__main__':
    #dm = getFilesAndFoldersMap()
    print(getPrivateDataFilename())
