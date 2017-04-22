"""
Given a set of lines, offer to run one of the last 10.

# TODO

- Also support just copy to clipboard.
- Also able to provide suffix / prefix.
"""

import sys
import os 
import re
import argparse

_meta_shell_command = 'lrun'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--run_number', default=None, type=int)
    parser.add_argument('-p', '--prefix', default="", type=str)
    args = parser.parse_args()
    return args

def fromStdInIfData():
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None

if __name__ == '__main__':

    args = getArgs()

    data = fromStdInIfData()
    if data is None: exit(0)
    lines = data.splitlines()
    lines = lines[0:20]

    for i, l in enumerate(lines):
        print('%.2d: %s' % (len(lines) - i - 1, l))

    if args.run_number is not None:
        n = int(args.run_number)
        le = lines[len(lines) - n - 1]
        le = args.prefix + " " + le
        print('Executing `%s`.' % le)
        os.system(le)
