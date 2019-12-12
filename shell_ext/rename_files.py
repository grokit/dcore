#!/usr/bin/python3

"""
Rename files / folders with nice, commonly used patterns.

# TODO

- Prepend ISO date: 2014-01-01_<filename>
- Prepend common prefix: rename_files toto: a.jpg -> toto_a.jpg
- Pick folder name from photos folder: assuming lots of dates in files, just pick the most common one and rename folder with it.
"""

import re
import os
import argparse
import time

_meta_shell_command = 'rename_files'

def getArgs():
    parser = argparse.ArgumentParser()
    #parser.add_argument('mode', nargs='?', default='remove_spaces')
    parser.add_argument('mode', nargs='?', default='remove_aggressive')
    #parser.add_argument('mode', nargs='?', default='remove_non_az')
    parser.add_argument('rest', nargs='?')
    parser.add_argument('-a', '--apply', action='store_true', default=False, help='Apply.')
    args = parser.parse_args()
    return args

def isNum(s):
    try:
        int(s)
    except:
        return False
    return True

def removeSpace(filename, args):
    to = re.sub('[ ()]', '_', filename)

    L = []
    for i in range(0, len(to)):
        if i != len(to) - 1:
            if isNum(to[i]) and not isNum(to[i + 1]):
                if i == 0 or not isNum(to[i - 1]):
                    L.append('0')
        L.append(to[i])
    to = ''.join(L)
    return to

def removeAggressive(filename, args):
    v = set('abcdefghijklmnopqrstuvwxyz._ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789[]') # ()

    toLower = True

    fout = []
    for l in filename:
        if l in v:
            if toLower:
                l = l.lower()
            fout.append(l)
        else:
            if l == 'ä':
                fout.append('a')
            else:
                fout.append('_')
    return "".join(fout)

def prefix(f, arg):
    if arg is None:
        raise Exception('No country for None arg.')
    return "%s_%s" % (arg, f)

def suffix(f, arg):
    if arg is None:
        raise Exception('No country for None arg.')

    ext = ''
    if '.' in f:
        ext = f[f.rfind('.'):]
        f = f[:f.rfind('.')]

    return "%s_%s%s" % (f, arg, ext)

def date(f, arg):
    t=time.strftime('%Y-%m-%d')
    return "%s_%s" % (t, f)

def custom(f, arg):
    return f.replace('__', '_')

def order_by(f, arg):
    if '#' in f:
        n = int(f.split('#')[1].split('-')[0])
    else:
        n = 99
    return "%.2i_%s" % (n, f)

def changeExt(f, arg):
    return os.path.splitext(f)[0] + '.markdown'
    
if __name__ == '__main__':
    files = os.listdir('.')
    #files = [f for f in files if os.path.isfile(f)]

    fnMap = {
            'remove_spaces': removeSpace,
            'remove_aggressive': removeAggressive,
            'change_ext': changeExt,
            'prefix': prefix,
            'suffix': suffix,
            'date': date,
            'custom': custom,
            'order_by': order_by,
            }

    args = getArgs()
    mode = args.mode

    if mode not in fnMap:
        raise Exception('Error, mode not in map. Mode: %s, map: %s.' % (mode, ", ".join(fnMap.keys())))

    print('Applying %s.' % mode)
    fn = fnMap[mode] 

    for f in files:
        to = fn(f, args.rest)
        if f != to:
            print('%s -> %s' % (f, to))
            if args.apply:
                os.rename(f, to)
            else:
                print('Skipped since apply switch off.')
