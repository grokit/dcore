"""
vimt: open in vim tabs

The default mode is to take from stdin, fuzzy-find filenames then open them in vi.

Flow:

    find | grep pattern | vimt

# TODO-A

- Does it work on MacOS?


# Documentation on Other Implementations

Do not do:

    cmd = 'vim -p %s' % " ".join(files)
    You will get the following: `Vim: Warning: Input is not from a terminal os.command`
    See http://unix.stackexchange.com/questions/44426/xargs-and-vi-input-is-not-from-a-terminal

Can do this, but not portable to non-*nix:

    cmd = "xargs bash -c '</dev/tty vim -p %s'" % " ".join(files)
    print(cmd)
    os.system(cmd)
"""

import os
import sys
import glob
import argparse
import tempfile
import platform

import dcore.fuzzy_extract as fuzzy_extract

_meta_shell_command = 'vimt'

def get_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

def read_from_stdin():
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def open_in_vim(files):
    # For some odd reason, this does not work with writing file.
    # Have to use alternate opening strategy which is limited to some OS.
    if platform.system().lower() == 'linux':
        cmd = "xargs bash -c '</dev/tty vim -p %s'" % " ".join(files)
    else:
        cmd = 'echo %s | xargs -o vi -p' % " ".join(files)
    print(cmd)
    os.system(cmd)

def do():
    args = get_args()

    data = read_from_stdin()
    if data is None:
        print('No stdin data. This util expects data to be piped-in.')
        exit(-1)
    files = fuzzy_extract.extract_files_fuzzy(data)
    print(f'found: {files}')

    open_in_vim(files)

if __name__ == '__main__':
    do()
