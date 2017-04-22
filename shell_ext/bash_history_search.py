"""
"""

import sys
import os 
import re
import argparse

_meta_shell_command = 'hs'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cut_len', default=20, type=int)
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = getArgs()

    with open(os.path.expanduser('~/.bash_history'), 'r') as fh:
        lines = fh.readlines()

    # Remove multiple same commands in a row.
    L = []
    for i, l in enumerate(lines):
        if i == 0: continue
        if lines[i] != lines[i-1]:
            L.append(lines[i])
    lines = L

    lines = lines[-args.cut_len:]
    lines = [l for l in L if len(l) > 0 and l[0] != '#']
    for l in lines:
        l = l.strip()
        print(l)

