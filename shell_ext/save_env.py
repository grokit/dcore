"""
Create dcore script that saves tmux, bashrc, ... files somewhere. 

# TODO

- command to store, command to restore (and merge?)

"""

import os
import sys 
import time
import shutil

_meta_shell_command = 'save_env'

# Files or folders
SAVE_ME = [
    '~/.vim',
    '~/.i3',
    '~/.vimrc',
    '~/.tmux.conf',
    '~/.profile', # macos
    '~/.bashrc',
    '~/.irssi',
    '~/.inputrc'
    '~/.gnomerc',
    '~/.bash_history',
]

SAVE_ME_MEH = [
    '~/.viminfo', # not that useful, can likely contain private information.
]

# TODO:::b, THIS SHOULD BE INSIDE DCOREDATA, not some random place.
BACKUP_IN = '~/sync/archive/backups/auto/script-backup-env'

def saveDir(f, dst):
    dstName = os.path.split(f)[1] 
    src = f
    dst = os.path.join(dst, dstName)
    print('%s -> %s' % (src, dst))
    shutil.copytree(src, dst)

def saveFile(f, dst):
    dstName = os.path.split(f)[1] 
    src = f
    dst = os.path.join(dst, dstName)
    print('%s -> %s' % (src, dst))
    shutil.copy(src, dst)

if __name__ == '__main__':
    SAVE_ME = [os.path.expanduser(f) for f in SAVE_ME]
    SAVE_ME = [f for f in SAVE_ME if (os.path.isfile(f) or os.path.isdir(f))]
    BACKUP_IN = os.path.expanduser(BACKUP_IN)

    dst = os.path.join(BACKUP_IN, str(int(time.time()*1000)))

    for f in SAVE_ME:
        if os.path.isdir(f):
            saveDir(f, dst)
        elif os.path.isfile(f):
            saveFile(f, dst)
        else:
            raise Exception("Cannot save %s" % f)
