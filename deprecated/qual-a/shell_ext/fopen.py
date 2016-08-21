"""
# TODO

- Merge with dr: remember files and directories, allow to navigate and open in text editor.
"""

import os
import smtplib
import time
import argparse
import dcore.system_description as system_description

_meta_shell_command = 'fopen'

import os

def getArgs():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-l', '--list_files', action = "store_true")
    parser.add_argument('lookup', type=str, nargs='?')

    args = parser.parse_args()
    return args

def printlistFiles(D):
    print('Information from file: %s.' % system_description.getPrivateDataFilename())
    for k, v in D.items():
        print('%-20s: %s' % (k, os.path.realpath(v)))
    
if __name__ == '__main__':
    
    args = getArgs()
    print(args)

    editor = 'vim'
    
    items = system_description.getFilesAndFoldersMap().items()
    known = {k:v for (k,v) in items if os.path.isfile(v)}
    
    if args.list_files == True:
        print('Folders:\n')
        printlistFiles({k:v for (k,v) in items if os.path.isdir(v)})
        print('\nFiles:\n')
        printlistFiles(known)
        exit(0)
        
    known = {k:v for (k,v) in items if os.path.isfile(v)}
    

    
    target = args.lookup

    if known.get(target) is None:
	    raise Exception("Cannot find: %s." % target)

    cmd = '%s %s' % (editor, known[target])
    print(cmd)
    os.system(cmd)

