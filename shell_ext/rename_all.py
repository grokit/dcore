#!/usr/bin/python3
"""
Rename filenames and file content.
Applies recursively on all files by default.
"""

import re
import os
import argparse
import time

_meta_shell_command = 'rename_all'

DEBUG = True


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('f', help='from')
    parser.add_argument('t', help='to')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--nocontent', action='store_true')
    parser.add_argument('--nofilename', action='store_true')
    args = parser.parse_args()
    return args


def walkGatherAllFiles(rootdir='.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append(os.path.join(dirpath, f))
    return F


def containsHiddenFolder(filename):
    pre, fn = os.path.split(os.path.abspath(filename))
    pre = pre.split('/')
    for p in pre:
        if len(p) > 1 and p[0] == '.': return True
    return False


def renameFileContent(filename, frm, to):
    if DEBUG:
        print('renameFileContent ', filename)
    with open(filename, 'r') as fh:
        content = fh.read()
    with open(filename, 'w') as fh:
        content = content.replace(frm, to)
        fh.write(content)


def renameFilename(filename, frm, to):
    pre, fn = os.path.split(os.path.abspath(filename))
    fn = fn.replace(frm, to)
    fn = os.path.join(pre, fn)
    if DEBUG:
        print('renameFilename ', filename, fn)
    os.rename(filename, fn)


def getFiles():
    files = walkGatherAllFiles('.')

    F = []
    for f in files:
        if not containsHiddenFolder(f):
            F.append(f)
        else:
            if DEBUG:
                pass
                #print('Skipping ', f)
    return F


if __name__ == '__main__':
    args = getArgs()
    print(args)
    DEBUG = args.debug

    if False:
        args.f = ''
        args.t = ''

    if not args.nocontent:
        for f in getFiles():
            print(f)
            try:
                renameFileContent(f, args.f, args.t)
            except:
                print('Failed ', f)

    if not args.nofilename:
        for f in getFiles():
            try:
                renameFilename(f, args.f, args.t)
            except:
                print('Failed ', f)
