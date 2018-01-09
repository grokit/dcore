"""
Backups to a remote location.
Uses duplicity + backblaze b2 for storage.

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
    cmd = 'duplicity list-current-files %s' % url
    stdoutdata = subprocess.getoutput(cmd)
    print(stdoutdata)

def backup(url, fullpath, pw):
    os.environ['PASSPHRASE'] = pw
    cmd = 'duplicity %s %s --progress --volsize 25' % (fullpath, url)

    l = None
    for l in executeCmd(cmd):
        print(l.strip())

    os.environ['PASSPHRASE'] = 'None'
    # Note sure this works as intended (l contains last return = status code)
    if l != 0:
        raise Exception('Status: %s' % l)

if __name__ == '__main__':
    args = getArgs()
    pw, url = getBackupPWAndUrl()

    backup(url, os.path.abspath(os.path.expanduser('~/sync/dev/coding_practice')), pw)
    listFiles(url)

