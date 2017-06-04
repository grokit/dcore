"""
"""

import sys
import os 
import re
import argparse

_meta_shell_command = 'hs'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cut_len', default=60, type=int)
    parser.add_argument('filter', default = [], nargs='*')
    args = parser.parse_args()
    return args

def filterLine(l):
    if len(l) == 0: return True
    if len(l.strip()) == 0: return True
    if l[0] == '#': return True
    return False

if __name__ == '__main__':

    args = getArgs()

    with open(os.path.expanduser('~/.bash_history'), 'r') as fh:
        lines = fh.readlines()

    lines = [l.strip() for l in lines if not filterLine(l)]

    # Remove multiple same commands in a row.
    L = []
    for i, l in enumerate(lines):
        if i == 0: continue
        if lines[i] != lines[i-1]:
            L.append(lines[i])
    lines = L

    lfilter = " ".join(args.filter)
    print('Applying regex filter `%s`.' % lfilter)
    lines = [l for l in lines if re.search(lfilter, l) is not None]

    lines = lines[-args.cut_len:]
    for l in lines:
        print(l)

