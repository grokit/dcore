"""
# TODO
- Can list the shortcuts available
- Make this part of system setup & have the files in the global configure thingie.
- Be able to open my scripts shortcuts: if conflict in resolve, throw an exception (have a generic 'checkMatch()' algorithm).
"""

import os
import smtplib
import time
import argparse
import dcore.system_description as sd

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
    
    known = sd.getFilesMap()
    
    target = args.lookup[0]

    if known.get(target) is None:
	    raise Exception("Cannot find: %s." % target)

    cmd = '%s %s' % (editor, known[target])
    os.system(cmd)


