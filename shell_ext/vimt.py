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

_meta_shell_command = 'vimt'

def fromStdInIfData():
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None

def extractFilesFuzzy(lines):
    F = set()
    for l in lines:
        l = l.strip()
        if ':' in l:
            l = l.split(':')[0]
        if os.path.isfile(l):
            F.add(l)
    return F

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--str_match', default=False, help='Open all files which has str_match in.')
    parser.add_argument('-c', '--colon_open', action="store_true")
    return parser.parse_args()

def listFilesContainingString(s):
    """
    Look all files recursively and if has s, then return.
    """

    files = []
    for filename in glob.iglob('**/*.**', recursive=True):
        try:
            with open(filename) as fh:
                content = fh.read()
                if s in content:
                    files.append(filename)
        except:
            print('Skipping: %s.' % filename)
    return files

def colonOpen(s):
    return listFilesContainingString(':'*3)

def openFilesFromStdin():
    rd = fromStdInIfData()
    if rd is None:
        raise Exception("Not implemented: maybe some cool shortcut to open files in vim")

    files = extractFilesFuzzy(rd.splitlines())

    # For some odd reason, this does not work with writing file.
    # Have to use alternate opening strategy which is limited to some OS.
    cmd = "xargs bash -c '</dev/tty vim -p %s'" % " ".join(files)
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':

    args = getArgs()

    files = []
    if args.colon_open:
        files = colonOpen(args.str_match)
    elif args.str_match:
        files = listFilesContainingString(args.str_match)
    else:
        print('Reading from stdin...')
        openFilesFromStdin()
        exit(0)

    print('Using files: %s.' % files)
    if len(files) == 0:
        print('No files.')
        exit(0)
    elif len(files) > 50:
        print('Too many files, not opening.')
        exit(0)

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfile = tmpdirname + '/.vimf'
        open(tmpfile, 'w').write("\n".join(files))
        cmd = 'vi -p `cat %s`' % tmpfile
        print(cmd)
        os.system(cmd)

