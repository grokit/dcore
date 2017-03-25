"""
# File Filter

Extract filenames from fuzzy output, adding some guess along the way and only return fullpath to valid files.

# TODO
"""

import sys
import os 
import re

_meta_shell_command = 'ff'

def getArgs():
    parser = argparse.ArgumentParser()
    """
    parser.add_argument('grep', type=str, nargs='*', default = None)
    parser.add_argument('-r', '--reset', action="store_true", help="")
    """
    args = parser.parse_args()
    return args

def fromStdInIfData():
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None

def filterIsFile(f):
    if os.path.isfile(f):
        return f
    if os.path.isfile(os.path.expanduser(f)):
        return f
    return None

def gitStatusOutput(f):
    """
    M  a/b/c/file.py
    """
    if ' ' in f:
        p = f.find(' ')
        if p != len(f)-1:
            f = f[p+1:]

    return filterIsFile(f)

def missingHomePath(f):
    """
    folder/file.e when file is in ~/folder/file.e
    """
    return filterIsFile(os.path.join('~/', f))

# Applied in order until a match is found, so start by least-fuzzed to most fuzzed.
FILTERS = [
        filterIsFile,
        gitStatusOutput,
        missingHomePath,
    ]

def extractFileFuzzy(f):
    for filt in FILTERS:
        r = filt(f)
        if r is not None:
            return os.path.abspath(os.path.expanduser(r))
    return None

if __name__ == '__main__':
    data = fromStdInIfData()
    if data is None: exit(0)
    lines = data.splitlines()

    for l in lines:
        f = extractFileFuzzy(l)
        if f is not None:
            print(f)
