"""
usage:
    import logging 
    import dcore.dlogging as dlogging
    dlogging.setup()
    ...
    then just use the logging module
"""

import os
import logging
import datetime
import logging.handlers

import dcore.data as data


def date_now_for_annotation():
    return datetime.datetime.now().isoformat()

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
    logging.basicConfig(level=logging.INFO)
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
