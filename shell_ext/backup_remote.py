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

def listFiles(url):
    cmd = 'ls'
    stdoutdata = subprocess.getoutput(cmd)
    print(stdoutdata)

def init(pw, url):
    # THIS DIDN'T WORK, but worked when I ran from console.
    os.environ['BORG_PASSPHRASE'] = pw
    cmd = 'borg init %s' % (url)
    os.environ['BORG_PASSPHRASE'] = 'none'
    for l in executeCmd(cmd):
        print(l)
    print('done')

def backup(pw, url, pathToBackup):
    os.environ['BORG_PASSPHRASE'] = pw
    pathToBackup = os.path.abspath(os.path.expanduser(pathToBackup))
    cmd = "borg create %s::Test-%s %s" % (url, int(1000*time.time()), pathToBackup)
    for l in executeCmd(cmd):
        print(l.strip())
    os.environ['BORG_PASSPHRASE'] = 'none'
    print('done')

if __name__ == '__main__':
    args = getArgs()
    pw, url = getBackupPWAndUrl()

    #backup(url, os.path.abspath(os.path.expanduser('~/sync')), pw)
    #listFiles(url)
    init(pw, url)
    #backup(pw, url, '~/Documents')

