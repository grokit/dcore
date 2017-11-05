#!/usr/bin/python3

"""
Rename filenames and file content.
"""

import re
import os
import argparse
import time

_meta_shell_command = 'rename_all'

def walkGatherAllFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append( os.path.join(dirpath, f) )
    return F

def getArgs():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args

def containsHiddenFolder(filename):
    pre, fn = os.path.split(os.path.abspath(filename))
    pre = pre.split('/')
    for p in pre:
        if len(p) > 1 and p[0] == '.': return True
    return False

if __name__ == '__main__':
    files = walkGatherAllFiles('.')
    files = [f for f in files if not containsHiddenFolder(f)]

    for f in files:
        print(f)

