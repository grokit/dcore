"""

# TODO

- Known bug where sometimes it locks on very long runned session.

"""

import logging
import subprocess

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

