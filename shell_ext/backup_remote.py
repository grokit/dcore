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
import datetime

import dcore.files as files
import dcore.private_data as private_data
import dcore.apps.gmail.gmail as gmail

_meta_shell_command = 'backup_remote'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--init', action="store_true")
    parser.add_argument('-s', '--snapshots_list', action="store_true")
    parser.add_argument('-l', '--ls', action="store_true")
    parser.add_argument('-m', '--mount', action="store_true")
    parser.add_argument('-u', '--umount', action="store_true")
    args = parser.parse_args()
    return args

def getBackupPWAndUrl():
    return private_data.k_remote_backup_backblaze_v1, private_data.backblaze_b2_url

def dateForAnnotation():
    #int(1000*time.time())
    #return datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
    return datetime.datetime.now().isoformat()

def executePrintAndReturn(cmd):
    L = []
    for l in executeCmd(cmd):
        L.append(l)
        print(l.strip())
    return "".join(L)

def executeCmd(cmd):
    print('Executing: %s.' % cmd)

    if True:
        cmd = cmd.split(' ')
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for l in p.stdout:
            yield l
        p.stdout.close()
        return p.wait()

def listSnapshots(url):
    cmd = 'borg list %s --short' % (url)
    return executePrintAndReturn(cmd)

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
    executePrintAndReturn(cmd)

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
    cmd = 'borg umount /media/borg'
    for l in executeCmd(cmd):
        print(l.strip())

def backup(pw, url, pathToBackup):
    pathToBackup = os.path.abspath(os.path.expanduser(pathToBackup))
    # https://borgbackup.readthedocs.io/en/stable/usage/create.html
    # --list to print files as we process
    cmd = "borg create --stats --progress %s::AutoBackup-%s %s" % (url, dateForAnnotation(), pathToBackup)
    return executePrintAndReturn(cmd)

def sendMail(content):
    args = getArgs()
    title = "Backup Report m3pzBxlKu %s" % dateForAnnotation()
    gmail.sendEmail(private_data.primary_email, title, content)

def report(content):
    if True:
        try:
            sendMail(content)
        except Exception as e:
            print(e)
    
def default():
    pw, url = getBackupPWAndUrl()
    # With server version, this does not return anything.
    backup(pw, url, '~/sync')
    stdout = listSnapshots(url)
    report(stdout)

def do():
    args = getArgs()
    pw, url = getBackupPWAndUrl()

    os.environ['BORG_PASSPHRASE'] = pw
    try:
        if args.ls:
            snapshot = getLastSnapshot(url)
            listFiles(url, snapshot)
        elif args.snapshots_list:
            for l in listSnapshots(url):
                print(l)
        elif args.init:
            init(pw, url)
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

def test():
    pw, url = getBackupPWAndUrl()
    os.environ['BORG_PASSPHRASE'] = pw
    cmd = 'borg list %s --short' % (url)
    stdout = executePrintAndReturn(cmd)
    print('---')
    print(stdout)
    report(stdout)

if __name__ == '__main__':
    do()
    #test()
