"""
vimt: fuzzy-extract files and folders from input.
"""

import os
import sys
import re
import argparse

_meta_shell_command = 'fextract'


def getArgs():
    parser = argparse.ArgumentParser()
    #parser.add_argument('-s', '--str_match', default=False, help='Open all files which has str_match in.')
    #parser.add_argument('-c', '--colon_open', action="store_true")
    return parser.parse_args()


def fromStdInIfData():
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def fuzzyExtractFolderFromLine(line):
    if os.path.isdir(line): return line
    folders = []

    # Look for folder name between spaces.
    for p in line.split(' '):
        if os.path.isdir(p):
            folders.append(p)

        # If file, extract folder.
        if os.path.isfile(p):
            p = os.path.split(p)[0]
            if os.path.isdir(p):
                folders.append(p)

    return folders


if __name__ == '__main__':

    args = getArgs()

    rd = fromStdInIfData()
    if rd is None:
        raise Exception("No stdin data.")

    folders = []
    for line in rd.splitlines():
        folders += fuzzyExtractFolderFromLine(line)

    for f in folders:
        print(f)
