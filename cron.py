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

def task_digest():
    def fn():
        import dcore.apps.notes_db.commands.digest as note_db_digest
        note_db_digest.do()

    do_every.rateLimitPerHour('digest', 19, fn)

def task_keyfile():
    import dcore.private_data as private_data
    import dcore.apps.gmail.gmail as gmail
    keyfile = private_data.filename_keyfile
    keyfile = os.path.abspath(os.path.expanduser(keyfile))

    if do_every.isFileModifiedSinceLastTouch(keyfile):
        gmail.sendEmail(private_data.primary_email, "KeyFile UAOfzxsK %s" % time.time(), "See file.", filenameAttach=keyfile)
        do_every.markFileAsCurrent(keyfile)
        logging.debug('Keyfile updated.')
    else:
        logging.debug('Skipping keyfile, did not change.')

def task_backup():
    def fn():
        import dcore.apps.backup_remote.backup_remote as backup_remote
        backup_remote.do()

    do_every.rateLimitPerHour('backup_remote', 18, fn)

if __name__ == '__main__':
    dlogging.setup()

    runme = []
    runme.append(task_keyfile)
    runme.append(task_backup)
    runme.append(task_digest)

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

