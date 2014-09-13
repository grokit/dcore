"""
# TODO
- Can list the shortcuts available
- Make this part of system setup & have the files in the global configure thingie.
- Be able to open my scripts shortcuts: if conflict in resolve, throw an exception (have a generic 'checkMatch()' algorithm).
- fopen new file_abc <-- abc gets created and automatically accessible by the next fopen file_abc
- fopen --list
"""

import os
import smtplib
import time
import argparse
import dcore.system_description as system_description

_meta_shell_command = 'fopen'

def getArgs():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-l', '--list', action = "store_true")
    parser.add_argument('lookup', type=str, nargs='?')

    args = parser.parse_args()
    return args

def printList(D):
    
    for k, v in D.items():
        print('%-20s: %s' % (k, v))
    
if __name__ == '__main__':
    
    args = getArgs()
    print(args)

    editor = 'vim'
    
    known = system_description.getFilesMap()
    
    if args.list == True:
        printList(known)
        exit(0)
    
    target = args.lookup

    if known.get(target) is None:
	    raise Exception("Cannot find: %s." % target)

    cmd = '%s %s' % (editor, known[target])
    os.system(cmd)


