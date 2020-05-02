import os
import logging
import datetime
import logging.handlers

import dcore.data as data


def dateForAnnotation():
    return datetime.datetime.now().isoformat()


def filterLog(logAsStr):
    """
    Nice to have in reverse order in mail client.
    """
    log_lines = logAsStr.splitlines()
    log_lines.reverse()

    out = []
    isErr = False
    for line in log_lines:
        if '- ERROR -' in line:
            out.append(line)
            isErr = True
    return isErr, "\n".join(out)



def genLogFilename():
    """
    This only works for long-lived processes:
    rFileHandler = logging.handlers.TimedRotatingFileHandler(logFilename, when='D', interval=1)

    ... so basically just pick a log name file that merges together by hour.
    """
    if True:
        return 'dcore.%s.log' % datetime.datetime.now().strftime(
            "%Y-%m-%d_%H:%M.%S.%f")
    else:
        return 'dcore.%s.log' % datetime.datetime.now().strftime(
            "%Y-%m-%d_%H:00.000")


def setup():
    logging.basicConfig(level=logging.DEBUG)
    folder = data.logsdir()
    data.createDirIfNotExist(folder)

    logFilename = os.path.join(folder, genLogFilename())

    # Safety measure: dlogging should not be used for long-lived processes, but in case it happens,
    # roll the log every day.
    rFileHandler = logging.handlers.TimedRotatingFileHandler(logFilename,
                                                             when='D',
                                                             interval=1)

    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rFileHandler.setFormatter(formatter)

    rootLogger = logging.getLogger('')
    rootLogger.addHandler(rFileHandler)


if __name__ == '__main__':
    setup()
