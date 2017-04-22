"""
"""

import sys
import os 
import re
import argparse

_meta_shell_command = 'hs'

def getArgs():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = getArgs()

    with open(os.path.expanduser('~/.bash_history'), 'r') as fh:
        lines = fh.readlines()

    lines = lines[-20:]
    for l in lines:
        l = l.strip()
        print(l)

