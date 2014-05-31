"""
# TODO
- Can list the shortcuts available
- Make this part of system setup & have the files in the global configure thingie.

"""

import os
import smtplib
import time
import argparse

_meta_shell_command = 'fopen'
def getArgs():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('lookup', type=str, nargs='+')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    
    args = getArgs()
    print(args)

    editor = 'vim'

    known = {'todo': '/home/david/Desktop/Dropbox/logs/Todo_Home.txt',
             'ta': '/home/david/Desktop/Dropbox/logs/TheArchive.txt',
             'someday': '/home/david/Desktop/Dropbox/logs/MaybeSomeday.txt'}
    
    target = args.lookup[0]

    if known.get(target) is None:
	    raise Exception("Cannot find: %s." % target)

    cmd = '%s %s' % (editor, known[target])
    os.system(cmd)


