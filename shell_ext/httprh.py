"""
HTTP Remove Headers
"""

import os
import argparse
import re

_meta_shell_command = 'httprh'

def getArgs():

    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    
    args = getArgs()
    
    fh = open(args.file, 'r', encoding="ASCII")
    fc = fh.readlines()
    fh.close()
    
    fo = []
    for line in fc:
        lp = line
        line = re.sub(r"^([\w-]*?):(.*)\n", r"\1: ", line)
        if lp != line:
            #line = "%-20s [Removed]\n" % line
            line = None # Just remove headers.
        
        if line != None:
            fo.append(line)
    
    fo = "".join(fo)
    print(fo)



