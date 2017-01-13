"""
"""

import os
import time
import argparse
import sys

_meta_shell_command = 'sshot'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--open_last', action="store_true", default=False)
    parser.add_argument('-e', '--edit_last', action="store_true", default=False)
    parser.add_argument('-l', '--list', action="store_true", default=False)

    # Move all recent screenshots to current directory:
    # sshot -r | xargs mv -t .
    parser.add_argument('-r', '--list_recent', action="store_true", default=False)
    args = parser.parse_args()
    return args
    
IS_SSHOT = ['vlcsnap', 'Selection', 'scrot']

def screenshotsFilenameByModDate():
    loc = os.path.expanduser('~/Pictures')
    sshots = os.listdir(loc)
    sshots = [os.path.abspath(os.path.join(loc, f)) for f in sshots]

    T = set()
    for pre in IS_SSHOT:
        for f in sshots:
            if pre in f:
                T.add(f)
    sshots = list(T)

    # Get last modified file that matched pattern.
    sshots.sort(key=lambda x: os.path.getmtime(x))
    return sshots

if __name__ == '__main__':
    
    args = getArgs()

    if args.list:
        L = screenshotsFilenameByModDate()
        L.sort(key=lambda x: os.path.getmtime(x))
        for l in L:
            print(l)
        sys.exit(0)

    if args.list_recent:
        L = screenshotsFilenameByModDate()
        tnow = time.time()
        delta_hours = 2
        L = [l for l in L if tnow - os.path.getmtime(l) < delta_hours * 60 * 60]
        L.sort(key=lambda x: os.path.getmtime(x))
        for l in L:
            print(l)
        sys.exit(0)

    if args.open_last or args.edit_last:
        sshots = screenshotsFilenameByModDate()
        cmd = 'eog %s' % sshots[-1]
        if args.edit_last:
            cmd = 'shotwell %s' % sshots[-1]
        print(cmd)
        os.system(cmd)
        sys.exit(0)

    cmd = "scrot -e 'mv $f ~/Pictures'"
    print(cmd)
    r = os.system(cmd)
    if r != 0:
        raise Exception('sshot failed.')
    os.system('notify-send --icon=gtk-info sshot "Screenshot taken: %s."' % screenshotsFilenameByModDate()[-1])

