"""
Create dcore script that saves tmux, bashrc, ... files somewhere. 

# TODO

- command to store, command to restore (and merge?)

"""

import os
import sys
import time
import shutil

import dcore.data as data

_meta_shell_command = 'backup_env'

# Files or folders
SAVE_ME = [
    '~/.vim',
    '~/.i3',
    '~/.vimrc',
    '~/.tmux.conf',
    '~/.profile',  # macos
    '~/.bashrc',
    '~/.irssi',
    '~/.ssh',
    '~/.inputrc',
    '~/.config/i3',  # i3
    '~/.gnomerc',
    '~/.bash_history',
    '~/.config/liferea',
    '~/.local/share/Anki2',
    '~/.local/share/QuiteRss',
]

SAVE_ME_MEH = [
    '~/.viminfo',  # not that useful, can likely contain private information.
]


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
    BACKUP_IN = data.dcoreBackupEnv()

    SAVE_ME = [os.path.expanduser(f) for f in SAVE_ME]
    SAVE_ME = [f for f in SAVE_ME if (os.path.isfile(f) or os.path.isdir(f))]
    BACKUP_IN = os.path.expanduser(BACKUP_IN)

    dst = os.path.join(BACKUP_IN, str(int(time.time() * 1000)))

    for f in SAVE_ME:
        if os.path.isdir(f):
            saveDir(f, dst)
        elif os.path.isfile(f):
            saveFile(f, dst)
        else:
            raise Exception("Cannot save %s" % f)
