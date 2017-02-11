"""
vimt: open in vim tabs

Flow:

    ack <query> | vimt
    ack -g <query> | vimt
"""

import os
import sys

_meta_shell_command = 'vimt'

def fromStdInIfData():
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None

def extractFilesFuzzy(lines):
    F = []
    for l in lines:
        l = l.strip()
        if ':' in l:
            l = l.split(':')[0]
        if os.path.isfile(l):
            F.append(l)
    return F

if __name__ == '__main__':

    rd = fromStdInIfData()
    if rd is None:
        raise Exception("Not implemented: maybe some cool shortcut to open files in vim")

    files = extractFilesFuzzy(rd.splitlines())

    # Do not do:
    # cmd = 'vim -p %s' % " ".join(files)
    # You will get the following: `Vim: Warning: Input is not from a terminal os.command`
    # See http://unix.stackexchange.com/questions/44426/xargs-and-vi-input-is-not-from-a-terminal
    # On macosx maybe just -o
    cmd = "xargs bash -c '</dev/tty vim -p %s'" % " ".join(files)
    print(cmd)
    os.system(cmd)

