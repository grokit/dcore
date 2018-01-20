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
import logging
import difflib

import dcore.files as files
import dcore.private_data as private_data
import dcore.do_every as do_every 
import dcore.dlogging as dlogging
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
    return datetime.datetime.now().isoformat()

def executePrintAndReturn(cmd):
    L = []
    for l in executeCmd(cmd):
        L.append(l)
        print(l.strip())
    return "".join(L)

def executeCmd(cmd):
    logging.debug('Executing: %s.' % cmd)

    if True:
        cmd = cmd.split(' ')
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for l in p.stdout:
            yield l
        p.stdout.close()
        return p.wait()

def diff(url):
    """
    This doesn't work with current version.
    """
    snapshotsList = listSnapshots(url)
    if len(snapshotsList) < 2:
        logging.warning('Not enough backups to diff.')
        return
    cmd = 'borg diff %s::%s %s' % (url, snapshotsList[-2], snapshotsList[-1])
    return executePrintAndReturn(cmd)


def listSnapshots(url):
    cmd = 'borg list %s --short' % (url)
    return executePrintAndReturn(cmd)

def info(url):
    snapshot = getLastSnapshot(url)
    cmd = 'borg info %s::%s' % (url, snapshot)
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
    #cmd = 'borg list --short %s::%s' % (url, snapshot)
    cmd = 'borg list %s::%s' % (url, snapshot)
    return executePrintAndReturn(cmd)

def init(pw, url):
    cmd = 'borg init %s' % (url)
    for l in executeCmd(cmd):
        logging.debug(l.strip())

def mount(pw, url):
    snapshot = getLastSnapshot(url)
    cmd = 'borg mount %s::%s /media/borg' % (url, snapshot)
    for l in executeCmd(cmd):
        logging.debug(l.strip())

def umount(pw, url):
    cmd = 'borg umount /media/borg'
    for l in executeCmd(cmd):
        logging.debug(l.strip())

def notifyGMail(head, content):
    title = 'Backup Remote rZ5FTTdKiHHf2Z8t - %s' % head
    gmail.sendEmail(private_data.primary_email, title, content)

def backup(pw, url, pathToBackup):
    notifyGMail('Backup Starting', '')
    pathToBackup = os.path.abspath(os.path.expanduser(pathToBackup))
    # https://borgbackup.readthedocs.io/en/stable/usage/create.html
    # --list to logging.debug files as we process
    cmd = "borg create --stats --progress %s::AutoBackup-%s %s" % (url, dateForAnnotation(), pathToBackup)
    r = executePrintAndReturn(cmd)
    notifyGMail('Backup Done', r)
    return r

def default():
    pw, url = getBackupPWAndUrl()

    snapshot = getLastSnapshot(url)
    fileLstA = listFiles(url, snapshot)

    # With server version, this does not return anything.
    backup(pw, url, '~/sync')

    # Hmmmm but this will return even backup didn't run successfully.
    stdout = "Backup Report:\n"
    # stdout += listSnapshots(url)
    stdout += "\n" + info(url)

    snapshot = getLastSnapshot(url)
    fileLstB = listFiles(url, snapshot)

    # Borg diff doesn't work with current version.
    #d = difflib.Differ()
    #r = d.compare(fileLstA.splitlines(),fileLstB.splitlines())
    r = difflib.unified_diff(fileLstA.splitlines(),fileLstB.splitlines())
    stdout += "\nDiff:\n\n" + "\n".join(list(r))

    logging.info(stdout)

def do():
    dlogging.setup()
    args = getArgs()
    pw, url = getBackupPWAndUrl()

    os.environ['BORG_PASSPHRASE'] = pw
    try:
        if args.ls:
            snapshot = getLastSnapshot(url)
            listFiles(url, snapshot)
        elif args.snapshots_list:
            listSnapshots(url)
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
        logging.debug(e)
    os.environ['BORG_PASSPHRASE'] = 'none'

if __name__ == '__main__':
    do()
