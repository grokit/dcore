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
    parser.add_argument('-e', '--execute', action='store_true')
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

    lines = [l.strip().lower() for l in lines if not filterLine(l)]

    lfilter = " ".join(args.filter)
    print('Applying regex filter `%s`.' % lfilter)
    lines = [l for l in lines if re.search(lfilter, l) is not None]

    # Remove multiple same commands in a row.
    L = []
    for i, l in enumerate(lines):
        if i == 0: continue
        if lines[i] != lines[i-1]:
            L.append(lines[i])
    lines = L

    cut = len(lines)
    if args.cut_len < len(lines):
        cut = args.cut_len
        lines = lines[-cut:]

    if args.execute:
        for i, l in enumerate(lines):
            i = cut - i
            print('%.2i: %s' % (i,l))
        s = input('\nEnter number of execute.\n')
        if s == '':
            exit(0)
        s = cut - int(s)
        cmd = lines[s]
        print('Executing `%s`.'%cmd)
        os.system(cmd)
    else:
        for l in lines:
            print(l)

