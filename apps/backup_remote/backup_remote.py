"""
Backups to a remote location.

# TODO

# Troubleshooting

('Remote Exception (see remote log for the traceback)', 'LockTimeout')
    --> borg break-lock URL 
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
import dcore.osrun as osrun

_meta_shell_command = 'backup_remote'

BACKUP_ROOT = '~/sync'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action="store_true", help='For debugging.')
    parser.add_argument('-b', '--backup', action="store_true")
    parser.add_argument('-i', '--init', action="store_true")
    parser.add_argument('-s', '--list_snapshots', action="store_true")
    parser.add_argument('-z', '--list_snapshots_last', action="store_true")
    parser.add_argument('-l', '--list_files', action="store_true")
    parser.add_argument('-d', '--diff', action="store_true")
    parser.add_argument('-r', '--raw_command', help='Just run the command with password as environment variable. `URL` will be replaced by url.')
    parser.add_argument('-m', '--mount', action="store_true")
    parser.add_argument('-u', '--umount', action="store_true")
    args = parser.parse_args()
    return args

def getBackupPWAndUrl():
    return private_data.k_remote_backup_rsyncnet_v1, private_data.rsyncnet_url
    #return private_data.k_remote_backup_rsyncnet_v1, '/home/arch/tmp-borg'

def dateForAnnotation():
    return datetime.datetime.now().isoformat()

def diff(url):
    """
    This doesn't work with current version.
    """
    snapshotsList = listSnapshots(url)
    if len(snapshotsList) < 2:
        logging.warning('Not enough backups to diff.')
        return
    cmd = 'borg diff %s::%s %s' % (url, snapshotsList[-2], snapshotsList[-1])
    return osrun.executePrintAndReturnStdout(cmd)

def listSnapshots(url):
    cmd = 'borg list %s --short' % (url)
    return osrun.executePrintAndReturnStdout(cmd, doLog=False, doPrint=True)

def info(url):
    snapshot = getLastSnapshot(url)
    cmd = 'borg info %s::%s' % (url, snapshot)
    return osrun.executePrintAndReturnStdout(cmd)

def getLastSnapshot(url):
    cmd = 'borg list %s --short' % (url)
    stdout = osrun.executePrintAndReturnStdout(cmd, doLog=False, doPrint=False)
    snapshots = stdout.splitlines()
    snapshots = [s.strip() for s in snapshots]
    if len(snapshots) < 1:
        raise Exception('Cannot get last snapshot from output: %s.' % snapshots)
    return snapshots[-1]

def listFiles(url, snapshot):
    cmd = 'borg list %s::%s' % (url, snapshot)
    return osrun.executePrintAndReturnStdout(cmd, doLog=False, doPrint=False)

def init(url):
    cmd = 'borg init --encryption=repokey %s' % (url)
    return osrun.executePrintAndReturnStdout(cmd)

def mount(url):
    snapshot = getLastSnapshot(url)
    #snapshot = 'AutoBackup-2018-01-15T22:17:02.676038'
    cmd = 'borg mount %s::%s /media/borg' % (url, snapshot)
    osrun.executePrintAndReturnStdout(cmd)

def umount(url):
    cmd = 'borg umount /media/borg'
    osrun.executePrintAndReturnStdout(cmd)

def notifyGMail(head, content):
    title = 'Backup Remote rZ5FTTdKiHHf2Z8t - %s (%s)' % (head, dateForAnnotation())
    gmail.sendEmail(private_data.primary_email, title, content)

def backup(url, pathToBackup):
    pathToBackup = os.path.abspath(os.path.expanduser(pathToBackup))
    # https://borgbackup.readthedocs.io/en/stable/usage/create.html
    # --list to logging.debug files as we process
    cmd = "borg create -v --progress %s::AutoBackup-%s %s" % (url, dateForAnnotation(), pathToBackup)
    #return osrun.executePrintAndReturnStdout(cmd, doLog=False)

    # This:
    # osrun.executePrintAndReturnStdout(cmd, doLog=False)
    # ... gets stuck for some reason (only on borg create). 
    # May be because of NCurse being used to update count.
    # ... could try disabling progress too...
    os.system(cmd)
    return "osrun disabled for main backup command"

def default():
    notifyGMail('Backup Starting', '')
    pw, url = getBackupPWAndUrl()

    try:
        snapshotA = getLastSnapshot(url)
        fileLstA = listFiles(url, snapshotA)
    except Exception as e:
        logging.warning(e)
        fileLstA = ''

    # With server version, this does not return anything.
    backup(url, BACKUP_ROOT)

    # Hmmmm but this will return even backup didn't run successfully.
    stdout = "Backup Report:\n"
    # stdout += listSnapshots(url)
    stdout += "\n" + info(url)

    snapshotB = getLastSnapshot(url)
    fileLstB = listFiles(url, snapshotB)

    stdout += 'SnapshotA: %s, SnapshotB: %s.\n' % (snapshotA, snapshotB)

    # Borg diff doesn't work with current version.
    r = difflib.unified_diff(fileLstA.splitlines(),fileLstB.splitlines())

    r = list(r)
    if False:
        stdout += 'Diff size before filter: %s.\n' % len(r)
        r = [x for x in r if '.git' not in x]
        r = [x for x in r if '_h_' not in x]
        r = [x for x in r if len(x) > 0 and (x[0] == '+' or x[0] == '-')]
        stdout += 'Diff size after filter: %s.\n' % len(r)
    else:
        stdout += '\nDiff size: %s.\n\n' % len(r)

    stdoutAll = stdout + "Diff:\n\n" + "\n".join(r)

    logging.info(stdoutAll)
    notifyGMail('Backup Done', stdout)

def testCommand(url):
    cmd = 'borg list %s' % (url)
    return osrun.executePrintAndReturnStdout(cmd)

def do():
    dlogging.setup()
    args = getArgs()
    pw, url = getBackupPWAndUrl()

    os.environ['BORG_PASSPHRASE'] = pw
    os.environ['BORG_REMOTE_PATH'] = 'borg1'
    try:
        if args.list_files:
            snapshot = getLastSnapshot(url)
            listFiles(url, snapshot)
        elif args.list_snapshots:
            listSnapshots(url)
        elif args.list_snapshots_last:
            last = getLastSnapshot(url)
            print('Last snapshot: `%s`.' % last)
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
        elif args.backup:
            backup(url, BACKUP_ROOT)
        elif args.test:
            testCommand(url)
        else:
            default()
    except Exception as e:
        os.environ['BORG_PASSPHRASE'] = 'none'
        os.environ['BORG_REMOTE_PATH'] = 'none'
        logging.error('Exception: %s.' % e)
        raise e
    os.environ['BORG_PASSPHRASE'] = 'none'
    os.environ['BORG_REMOTE_PATH'] = 'none'

if __name__ == '__main__':
    do()
