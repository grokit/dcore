"""
Rules:
- Obviously, just use this for low security stuff (such as added layer of security when sending as mail), passwords for accounts I do not care about, ...
- Always keep old key, but in comment (disable script using them).
- Keep key indication in backup name.

# TODO
- Merge with system_description.py
"""

import os
import json

#import dcore.system_description

def __loadPrivateFile():

    #fileMap = dcore.system_description.getFilesMap()
    #privateDataFile = fileMap['private_data']
    
    privateDataFile = '/home/david/Desktop/Dropbox/scripts/private_data'

    fh = open(privateDataFile, 'r')
    jr = fh.read()
    fh.close()
    
    jd = json.loads(jr)

    return jd

def getDirsMapPrivate():
    jd = __loadPrivateFile()
    dirsMap = jd[os.name]
    return dirsMap

# This will add all the variables declared in the JSON file as local variables.
# This way, private_data.variable is accessible after importing the module.
jd = __loadPrivateFile()
localsDir = locals()
for k, v in jd['variables'].items():
    localsDir[k] = v

if __name__ == '__main__':
    dm = getDirsMapPrivate()
    #print(dm)
