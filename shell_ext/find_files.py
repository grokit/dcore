
import os
import argparse
import pickle

_meta_shell_command = 'ff'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('grep', type=str, nargs='?', default = None)
    parser.add_argument('-f', '--filenames_only', action="store_true")
    args = parser.parse_args()
    return args

def getAllFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append( os.path.join(dirpath, f) )
    return F

def elementInList(f, filterArray):
    for e in filterArray:
        if e in f:
            return True
    return False

def filterOutIfArrayInElement(F, filterArray):
    return [f for f in F if not elementInList(f, filterArray)]

def filterInCaseInsensitive(F, astr):
    return [f for f in F if astr in f.lower()]

def do():
    args = getArgs()

    F = getAllFiles(os.path.expanduser('~/sync'))
    F = filterOutIfArrayInElement(F, ['.git', '__pycache__'])

    if args.grep is not None:
        args.grep = args.grep.lower()
        print('Filter-in with: %s.' % args.grep)
        F = filterInCaseInsensitive(F, args.grep)

    for f in F:
        print(f)

if __name__ == '__main__':
    do()
