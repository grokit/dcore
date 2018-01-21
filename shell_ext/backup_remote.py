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
    parser.add_argument('-d', '--diff', action="store_true")
    parser.add_argument('-r', '--raw_command', help='Just run the command with password as environment variable. `URL` will be replaced by url.')
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

def rawCommand(url, cmd):
    """
    :::EXPERIMENTAL
    """
    cmd = cmd.replace('URL', url)
    return executePrintAndReturn(cmd)

def diff(url):
    """
    This doesn't work with current version.
    """
    snapshotsList = listSnapshots(url)
    if len(snapshotsList) < 2:
        logging.warning('Not enough backups to diff.')
        return
    cmd = 'borg diff --remote-path=borg1 %s::%s %s' % (url, snapshotsList[-2], snapshotsList[-1])
    return executePrintAndReturn(cmd)

def listSnapshots(url):
    cmd = 'borg list %s --remote-path=borg1 --short' % (url)
    return executePrintAndReturn(cmd)

def info(url):
    snapshot = getLastSnapshot(url)
    cmd = 'borg info --remote-path=borg1 %s::%s' % (url, snapshot)
    return executePrintAndReturn(cmd)

def getLastSnapshot(url):
    cmd = 'borg list %s --remote-path=borg1 --short' % (url)
    last = None
    for l in executeCmd(cmd):
        last = l.strip()

    if last is None:
        raise Exception()
    return last

def listFiles(url, snapshot):
    #cmd = 'borg list --short %s::%s' % (url, snapshot)
    cmd = 'borg list --remote-path=borg1 %s::%s' % (url, snapshot)
    return executePrintAndReturn(cmd)

def init(url):
    cmd = 'borg init --remote-path=borg1 %s' % (url)
    for l in executeCmd(cmd):
        logging.debug(l.strip())

def mount(url):
    snapshot = getLastSnapshot(url)
    #snapshot = 'AutoBackup-2018-01-15T22:17:02.676038'
    cmd = 'borg mount --remote-path=borg1 %s::%s /media/borg' % (url, snapshot)
    for l in executeCmd(cmd):
        logging.debug(l.strip())

def umount(url):
    cmd = 'borg umount --remote-path=borg1 /media/borg'
    for l in executeCmd(cmd):
        logging.debug(l.strip())

def notifyGMail(head, content):
    title = 'Backup Remote rZ5FTTdKiHHf2Z8t - %s (%s)' % (head, dateForAnnotation())
    gmail.sendEmail(private_data.primary_email, title, content)

def backup(url, pathToBackup):
    pathToBackup = os.path.abspath(os.path.expanduser(pathToBackup))
    # https://borgbackup.readthedocs.io/en/stable/usage/create.html
    # --list to logging.debug files as we process
    cmd = "borg create --remote-path=borg1 --stats --progress %s::AutoBackup-%s %s" % (url, dateForAnnotation(), pathToBackup)
    return executePrintAndReturn(cmd)

def default():
    notifyGMail('Backup Starting', '')
    pw, url = getBackupPWAndUrl()

    snapshot = getLastSnapshot(url)
    fileLstA = listFiles(url, snapshot)

    # With server version, this does not return anything.
    backup(url, '~/sync')

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

    r = list(r)
    r = [x for x in r if '.git' not in x]
    r = [x for x in r if '_h_' not in x]

    stdout += "\nDiff:\n\n" + "\n".join(r)

    logging.info(stdout)
    notifyGMail('Backup Done', stdout)

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
            init(url)
        elif args.diff:
            diff(url)
        elif args.mount:
            mount(url)
        elif args.umount:
            umount(url)
        elif args.raw_command:
            rawCommand(url)
        else:
            default()
    except Exception as e:
        os.environ['BORG_PASSPHRASE'] = 'none'
        logging.debug(e)
    os.environ['BORG_PASSPHRASE'] = 'none'

if __name__ == '__main__':
    do()
