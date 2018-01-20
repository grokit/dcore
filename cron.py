import os
import stat
import getpass
import datetime
import logging

import dcore.dlogging as dlogging
import dcore.do_every as do_every 

def install():
    fname = '/etc/cron.hourly/dcore_hourly'
    user = os.environ['SUDO_USER']
    cmd = "#!/bin/sh\nsu - __user__ -c '. ~/.bashrc && python3 __file__ |& tee -a ~/log_dcore_hourly.log'\n"
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

def backup():
    # TODO: generalize "do every x hours"
    key = 'backup_remote'
    freq = 6
    stats = object()
    if not do_every.isDoneInLastXHours(key, freq):
        import dcore.shell_ext.backup_remote as backup_remote
        backup_remote.do()
        do_every.markDone(key)
    else:
        logging.debug('Skipping backup, it was done %.2f hour(s) ago (doing every %.2f hour(s)).', do_every.lastTimeDone(key), freq)

if __name__ == '__main__':
    dlogging.setup()

    if True:
        backup()
        #install()
    else:
        logging.debug('Cron start')

        # List stuff to run.
        runme = [backup, dlogging.mirrorLogsToGMail]
        for r in runme:
            try:
                r()
            except Exception as e:
                logging.debug('cron job failed: %s (%s).' % (r, e))

        logging.debug('Cron end')

