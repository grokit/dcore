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
    args = parser.parse_args()
    return args

def getBackupPWAndUrl():
    return private_data.k_remote_backup_backblaze_v1, private_data.backblaze_b2_url

def executeCmd(cmd):
    cmd = cmd.split(' ')
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for l in p.stdout:
        yield l
    p.stdout.close()
    return p.wait()

def listSnapshots(url):
    os.environ['BORG_PASSPHRASE'] = pw
    cmd = 'borg list %s --short' % (url)
    for l in executeCmd(cmd):
        print(l)
    os.environ['BORG_PASSPHRASE'] = 'none'

def getLastSnapshot(url):
    os.environ['BORG_PASSPHRASE'] = pw
    cmd = 'borg list %s --short' % (url)
    last = None
    for l in executeCmd(cmd):
        last = l.strip()
    os.environ['BORG_PASSPHRASE'] = 'none'

    if last is None:
        raise Exception()
    return last

def listFiles(url, snapshot):
    os.environ['BORG_PASSPHRASE'] = pw
    cmd = 'borg list %s::%s' % (url, snapshot)
    for l in executeCmd(cmd):
        print(l.strip())
    os.environ['BORG_PASSPHRASE'] = 'none'

def init(pw, url):
    os.environ['BORG_PASSPHRASE'] = pw
    cmd = 'borg init %s' % (url)
    for l in executeCmd(cmd):
        print(l.strip())
    os.environ['BORG_PASSPHRASE'] = 'none'

def backup(pw, url, pathToBackup):
    os.environ['BORG_PASSPHRASE'] = pw
    pathToBackup = os.path.abspath(os.path.expanduser(pathToBackup))
    cmd = "borg create %s::Test-%s %s --stats --progress" % (url, int(1000*time.time()), pathToBackup)
    for l in executeCmd(cmd):
        print(l.strip())
    os.environ['BORG_PASSPHRASE'] = 'none'

if __name__ == '__main__':
    args = getArgs()
    pw, url = getBackupPWAndUrl()

    #init(pw, url)
    backup(pw, url, '~/sync/dev/coding_practice')
    snapshot = getLastSnapshot(url)
    listFiles(url, snapshot)

