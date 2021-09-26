import datetime
import os

import dcore.data as data

def dateForAnnotation():
    return datetime.datetime.now().isoformat()

def delCurrentShortcuts(tag):
    "Delete all files that have special marker inside output directory."
    scriptsOutputFolder = data.pathExt()
    
    for f in os.listdir(scriptsOutputFolder):
        f = os.path.join(scriptsOutputFolder, f)
        with open(f, 'r') as fh:
            fdata = fh.read()
        if tag in fdata:
            # print('Deleting script shortcut: %s.' % f)
            os.remove(f)


