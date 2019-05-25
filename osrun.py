"""

# TODO

- Known bug where sometimes it locks on very long runned session.

"""

import logging
import subprocess

def executeCmd(cmd, doPrint=False):
    # NCurse deadlock:
    # https://stackoverflow.com/questions/33886406/how-to-avoid-the-deadlock-in-a-subprocess-without-using-communicate
    cmd = cmd.split(' ')
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, close_fds=True)

    stdout = []
    stderr = []
    for l in p.stdout:
        stdout.append(l)
        if doPrint:
            print(l.strip())
    #p.stdout.close()
    for l in p.stderr:
        stderr.append(l)
        if doPrint:
            print(l.strip())
    #p.stderr.close()
    rv = p.wait()
    if rv != 0:
        raise Exception('Error value `%s` returned from `%s`.' % (rv, cmd))
    return rv, "".join(stdout), "".join(stderr)

def executePrintAndReturnStdout(cmd, doLog=True, doPrint=True):
    assert type(cmd) == type('')

    logging.debug('Executing: %s.' % cmd)
    L = []
    rv, stdout, stderr = executeCmd(cmd, doPrint)
    if doLog:
        logging.info(stdout)
        logging.warning(stderr)
    return stdout

def run_os(cmd):
    "Shortcut for above functions -- generally does the right thing."
    if type(cmd) == []:
        for lcmd in cmd:
            osrun.executePrintAndReturnStdout(lcmd)
    else:
	assert type(cmd) == type("")
        osrun.executePrintAndReturnStdout(cmd)

if __name__ == '__main__':
    pass

