"""
Given a set of lines, offer to run one of the last 10.

# TODO

- Also support just copy to clipboard.
- Also able to provide suffix / prefix.
"""

import sys
import os 
import re

_meta_shell_command = 'lrun'

def getArgs():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args

def fromStdInIfData():
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None

if __name__ == '__main__':
    data = fromStdInIfData()
    if data is None: exit(0)
    lines = data.splitlines()
    lines = lines[0:20]

    for l in lines:
        f = extractFileFuzzy(l)
        if f is not None:
            print(f)
