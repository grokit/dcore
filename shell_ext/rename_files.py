#!/usr/bin/python3

"""
Rename files / folders with nice, commonly used patterns.

# TODO

- Prepend ISO date: 2014-01-01_<filename>
- Prepend common prefix: rename_files toto: a.jpg -> toto_a.jpg
"""

import re
import os
import argparse
import time

_meta_shell_command = 'rename_files'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', nargs='?', default='remove_spaces')
    parser.add_argument('rest', nargs='?')
    args = parser.parse_args()
    return args

def isNum(s):
    try:
        int(s)
    except:
        return False
    return True

def removeSpace(filename, _):
    to = re.sub('[ ()]', '_', f)

    L = []
    for i in range(0, len(to)):
        if i != len(to) - 1:
            if isNum(to[i]) and not isNum(to[i + 1]):
                if i == 0 or not isNum(to[i - 1]):
                    L.append('0')
        L.append(to[i])
    to = ''.join(L)
    return to

def prefix(f, arg):
    if arg is None:
        raise Exception('No country for None arg.')
    return "%s_%s" % (arg, f)

def date(f, arg):
    t=time.strftime('%Y-%m-%d')
    return "%s_%s" % (t, f)

if __name__ == '__main__':
    files = os.listdir('.')
    files = [f for f in files if os.path.isfile(f)]

    fnMap = {
            'remove_spaces': removeSpace,
            'prefix': prefix,
            'date': date
            }

    args = getArgs()
    mode = args.mode

    if mode not in fnMap:
        print('Error, mode not in map. Mode: %s, map: %s.' % (mode, ", ".join(fnMap.keys())))

    print('Applying %s.' % mode)
    fn = fnMap[mode] 

    for f in files:
        to = fn(f, args.rest)
        print('%s -> %s' % (f, to))
        os.rename(f, to)


			
