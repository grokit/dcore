"""
"""

import os
import time
import argparse
import sys
import platform
import shutil

_meta_shell_command = 'sshot'

# Where system put screenshot. OK of some don't exist on some system, 
# will just get skipped. For write operation, uses FIRST valid folder.
SRC_FOLDER = ['~/Desktop/screenshots', '~/Pictures']
SRC_FOLDER = [os.path.expanduser(f) for f in SRC_FOLDER]
SRC_FOLDER = [f for f in SRC_FOLDER if os.path.isdir(f)]
SRC_FOLDER = SRC_FOLDER[0]

# Patterns that decide a file is a screenshot.
IS_SSHOT = ['vlcsnap', 'Selection', 'scrot', 'Screen']

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--open_last', action="store_true", default=False)
    parser.add_argument('-e', '--edit_last', action="store_true", default=False)
    parser.add_argument('-l', '--list', action="store_true", default=False)

    # Move all recent screenshots to current directory:
    # sshot -r | xargs mv -t .
    parser.add_argument('-r', '--list_recent', action="store_true", default=False)

    parser.add_argument('-c', '--copy_last_to_curr_dir', action="store_true", default=False, help='Copies the last screenshot taken to the current directory.')
    args = parser.parse_args()
    return args
    
def screenshotsFilenameByModDate():
    loc = SRC_FOLDER
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

def takeScreenshot():
    if platform.system() in ["macosx", "Darwin"]:
        raise Exception("On macos, just use command+shift+4.")

    cmd = "scrot -e 'mv $f %s'" % SRC_FOLDER
    print(cmd)
    bef = time.time()
    r = os.system(cmd)
    if r != 0:
        raise Exception('sshot failed.')

    file_written = screenshotsFilenameByModDate()[-1]
    assert bef < os.path.getmtime(file_written)
    os.system('notify-send --icon=gtk-info sshot "Screenshot taken: %s."' % file_written)

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

    if args.copy_last_to_curr_dir:
        last_ss = screenshotsFilenameByModDate()[-1]
        print('Copying %s to current directory.' % last_ss)
        shutil.copy(last_ss, '.')
        sys.exit(0)

    takeScreenshot()

