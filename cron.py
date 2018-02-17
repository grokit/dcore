import os
import time
import stat
import getpass
import datetime
import logging

import dcore.dlogging as dlogging
import dcore.do_every as do_every 

def install():
    fname = '/etc/cron.hourly/dcore_hourly'
    user = os.environ['SUDO_USER']
    cmd = "#!/bin/sh\nsu - __user__ -c '. ~/.bashrc && python3 __file__'\n"
    cmd = cmd.replace('__file__', os.path.abspath(__file__))

    # If run under sudo, would get root
    # user = getpass.getuser()
    cmd = cmd.replace('__user__', user)

    logging.debug(cmd)
    with open(fname, 'w') as fh:
        fh.write(cmd)

    st = os.stat(fname)
    # https://docs.python.org/3/library/stat.html
    os.chmod(fname, st.st_mode | stat.S_IEXEC | stat.S_IXOTH)

def task_sshots():
    pass

def task_keyfile():
    key = 'backup_keyfile'
    freq = 18
    if not do_every.isDoneInLastXHours(key, freq):
        import dcore.private_data as private_data
        import dcore.apps.gmail.gmail as gmail
        keyfile = private_data.filename_keyfile
        keyfile = os.path.abspath(os.path.expanduser(keyfile))
        gmail.sendEmail(private_data.primary_email, "KeyFile UAOfzxsK %s" % time.time(), "See file.", filenameAttach=keyfile)
        do_every.markDone(key)
    else:
        logging.debug('Skipping %s, it was done %.2f hour(s) ago (doing every %.2f hour(s)).', key, do_every.lastTimeDone(key), freq)

def task_backup():
    # TODO: generalize "do every x hours"
    key = 'backup_remote'
    freq = 18
    if not do_every.isDoneInLastXHours(key, freq):
        import dcore.apps.backup_remote.backup_remote as backup_remote
        backup_remote.do()
        do_every.markDone(key)
    else:
        logging.debug('Skipping %s, it was done %.2f hour(s) ago (doing every %.2f hour(s)).', key, do_every.lastTimeDone(key), freq)

if __name__ == '__main__':
    dlogging.setup()

    runme = []
    runme.append(task_backup)
    runme.append(task_keyfile)
    # Keep this last
    runme.append(dlogging.mirrorLogsToGMail)

    if False:
        install()
    else:
        logging.debug('Cron start')

        # List stuff to run.
        for r in runme:
            try:
                logging.debug('cron job starting: %s.' % (r))
                r()
            except Exception as e:
                logging.error('cron job failed: %s (%s).' % (r, e))

        logging.debug('Cron end')

