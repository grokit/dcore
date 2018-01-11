"""
Backups to a remote location.

# TODO
"""

import os
import shutil
import time
import argparse
import getpass
import subprocess

import dcore.files as files
import dcore.private_data as private_data

_meta_shell_command = 'backup_remote'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--ls', action="store_true")
    parser.add_argument('-m', '--mount', action="store_true")
    parser.add_argument('-u', '--umount', action="store_true")
    args = parser.parse_args()
    return args

def getBackupPWAndUrl():
    return private_data.k_remote_backup_backblaze_v1, private_data.backblaze_b2_url

def executeCmd(cmd):
    print('Executing: ', cmd)
    cmd = cmd.split(' ')
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for l in p.stdout:
        yield l
    p.stdout.close()
    return p.wait()

def listSnapshots(url):
    cmd = 'borg list %s --short' % (url)
    for l in executeCmd(cmd):
        print(l)

def getLastSnapshot(url):
    cmd = 'borg list %s --short' % (url)
    last = None
    for l in executeCmd(cmd):
        last = l.strip()

    if last is None:
        raise Exception()
    return last

def listFiles(url, snapshot):
    cmd = 'borg list %s::%s' % (url, snapshot)
    for l in executeCmd(cmd):
        print(l.strip())

def init(pw, url):
    cmd = 'borg init %s' % (url)
    for l in executeCmd(cmd):
        print(l.strip())

def mount(pw, url):
    snapshot = getLastSnapshot(url)
    cmd = 'borg mount %s::%s /media/borg' % (url, snapshot)
    for l in executeCmd(cmd):
        print(l.strip())

def umount(pw, url):
    cmd = 'borg umount %s /media/borg' % (url)
    for l in executeCmd(cmd):
        print(l.strip())

def backup(pw, url, pathToBackup):
    pathToBackup = os.path.abspath(os.path.expanduser(pathToBackup))
    cmd = "borg create %s::Test-%s %s --stats --progress" % (url, int(1000*time.time()), pathToBackup)
    for l in executeCmd(cmd):
        print(l.strip())

def default():
    pw, url = getBackupPWAndUrl()
    backup(pw, url, '~/sync/dev/2dgame')

if __name__ == '__main__':
    args = getArgs()
    pw, url = getBackupPWAndUrl()

    os.environ['BORG_PASSPHRASE'] = pw
    try:
        if args.ls:
            snapshot = getLastSnapshot(url)
            listFiles(url, snapshot)
        elif args.mount:
            mount(pw, url)
        elif args.umount:
            umount(pw, url)
        else:
            default()
    except Exception as e:
        os.environ['BORG_PASSPHRASE'] = 'none'
        print(e)
    os.environ['BORG_PASSPHRASE'] = 'none'



