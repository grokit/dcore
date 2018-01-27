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

_meta_shell_command = 'backup_remote'

BACKUP_ROOT = '~/sync'
#BACKUP_ROOT = '~/sync/dev/coding_practice'

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
    return private_data.k_remote_backup_backblaze_v1, private_data.backblaze_b2_url
    #return private_data.k_remote_backup_backblaze_v1, '/home/arch/tmp-borg'

def dateForAnnotation():
    return datetime.datetime.now().isoformat()

def executeCmd(cmd, doPrint=False):
    cmd = cmd.split(' ')
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    stdout = []
    stderr = []
    for l in p.stdout:
        stdout.append(l)
        if doPrint:
            print(l.strip())
    for l in p.stderr:
        stderr.append(l)
        if doPrint:
            print(l.strip())
    p.stdout.close()
    p.stderr.close()
    rv = p.wait()
    if rv != 0:
        raise Exception('Error value `%s` returned from `%s`.' % (rv, cmd))
    return rv, "".join(stdout), "".join(stderr)

def executePrintAndReturnStdout(cmd, doLog=True, doPrint=True):
    logging.debug('Executing: %s.' % cmd)
    L = []
    rv, stdout, stderr = executeCmd(cmd, doPrint)
    if doLog:
        logging.info(stdout)
        logging.warning(stderr)
    return stdout

def diff(url):
    """
    This doesn't work with current version.
    """
    snapshotsList = listSnapshots(url)
    if len(snapshotsList) < 2:
        logging.warning('Not enough backups to diff.')
        return
    cmd = 'borg diff %s::%s %s' % (url, snapshotsList[-2], snapshotsList[-1])
    return executePrintAndReturnStdout(cmd)

def listSnapshots(url):
    cmd = 'borg list %s --short' % (url)
    return executePrintAndReturnStdout(cmd, doLog=False, doPrint=True)

def info(url):
    snapshot = getLastSnapshot(url)
    cmd = 'borg info %s::%s' % (url, snapshot)
    return executePrintAndReturnStdout(cmd)

def getLastSnapshot(url):
    cmd = 'borg list %s --short' % (url)
    stdout = executePrintAndReturnStdout(cmd, doLog=False, doPrint=False)
    snapshots = stdout.splitlines()
    snapshots = [s.strip() for s in snapshots]
    if len(snapshots) < 1:
        raise Exception('Cannot get last snapshot from output: %s.' % snapshots)
    return snapshots[-1]

def listFiles(url, snapshot):
    cmd = 'borg list %s::%s' % (url, snapshot)
    return executePrintAndReturnStdout(cmd, doLog=False, doPrint=False)

def init(url):
    cmd = 'borg init --encryption=repokey %s' % (url)
    return executePrintAndReturnStdout(cmd)

def mount(url):
    snapshot = getLastSnapshot(url)
    #snapshot = 'AutoBackup-2018-01-15T22:17:02.676038'
    cmd = 'borg mount %s::%s /media/borg' % (url, snapshot)
    executePrintAndReturnStdout(cmd)

def umount(url):
    cmd = 'borg umount /media/borg'
    executePrintAndReturnStdout(cmd)

def notifyGMail(head, content):
    title = 'Backup Remote rZ5FTTdKiHHf2Z8t - %s (%s)' % (head, dateForAnnotation())
    gmail.sendEmail(private_data.primary_email, title, content)

def backup(url, pathToBackup):
    pathToBackup = os.path.abspath(os.path.expanduser(pathToBackup))
    # https://borgbackup.readthedocs.io/en/stable/usage/create.html
    # --list to logging.debug files as we process
    cmd = "borg create -v --progress %s::AutoBackup-%s %s" % (url, dateForAnnotation(), pathToBackup)
    return executePrintAndReturnStdout(cmd, doLog=False)

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
    #d = difflib.Differ()
    #r = d.compare(fileLstA.splitlines(),fileLstB.splitlines())
    r = difflib.unified_diff(fileLstA.splitlines(),fileLstB.splitlines())

    r = list(r)
    stdout += 'diff size before filter: %s\n' % len(r)
    r = [x for x in r if '.git' not in x]
    r = [x for x in r if '_h_' not in x]
    r = [x for x in r if len(x) > 0 and (x[0] == '+' or x[0] == '-')]
    stdout += 'diff size after filter: %s\n' % len(r)

    stdout += "\nDiff:\n\n" + "\n".join(r)

    logging.info(stdout)
    notifyGMail('Backup Done', stdout)

def testCommand(url):
    cmd = 'borg list %s' % (url)
    return executePrintAndReturnStdout(cmd)

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
