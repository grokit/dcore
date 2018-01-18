
import os
import logging
import datetime

from logging.handlers import TimedRotatingFileHandler

import dcore.data as data
import dcore.apps.gmail.gmail as gmail
import dcore.private_data as private_data
import dcore.do_every as do_every

def dateForAnnotation():
    return datetime.datetime.now().isoformat()

def mirrorLogsToGMail():
    folder = data.logsdir()

    for f in os.listdir(folder):
        f = os.path.join(folder, f)
        if do_every.isFileModifiedSinceLastTouch(f):
            print('Mirroring: %s' % f)
            title = "GMail Logs File Mirror m3pzBxlKu %s %s" % (dateForAnnotation(), f)
            with open(f, 'r') as fh:
                # What if file cannot be converted as str?
                gmail.sendEmail(private_data.primary_email, title, fh.read())
            do_every.markFileAsCurrent(f)
        else:
            print('Current: %s' % f)

class GMailHandler(logging.Handler):

    def emit(self, record):
        title = "GMail Handler m3pzBxlKu %s" % dateForAnnotation()
        msg = self.format(record)
        gmail.sendEmail(private_data.primary_email, title, msg)

def setup():
    logging.basicConfig(level=logging.DEBUG)
    folder = data.logsdir()
    data.createDirIfNotExist(folder)
    logFilename = os.path.join(folder, 'dcore.log')
    rFileHandler = TimedRotatingFileHandler(logFilename, when='M')
    rootLogger = logging.getLogger('')
    rootLogger.addHandler(rFileHandler)
    if False:
        rootLogger.addHandler(GMailHandler())

if __name__ == '__main__':
    setup()
    mirrorLogsToGMail()
    logging.info('test-append')

