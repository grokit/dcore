
import os
import logging
import datetime

from logging.handlers import TimedRotatingFileHandler

import dcore.data as data
import dcore.apps.gmail.gmail as gmail
import dcore.private_data as private_data

def dateForAnnotation():
    return datetime.datetime.now().isoformat()

def filterLog(logAsStr):
    """
    Nice to have in reverse order in mail client.
    """
    l = logAsStr.splitlines()
    l.reverse()
    return "\n".join(l)

def mirrorLogsToGMail():
    import dcore.do_every as do_every
    folder = data.logsdir()

    for f in os.listdir(folder):
        f = os.path.join(folder, f)
        if do_every.isFileModifiedSinceLastTouch(f):
            print('Mirroring: %s' % f)
            title = "GMail Logs File Mirror m3pzBxlKu %s %s" % (dateForAnnotation(), f)
            with open(f, 'r') as fh:
                # What if file cannot be converted as str?
                content = filterLog(fh.read())
                gmail.sendEmail(private_data.primary_email, title, content)
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
    rFileHandler = TimedRotatingFileHandler(logFilename, when='D', interval=1)

    # Format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rFileHandler.setFormatter(formatter)
    #logging.getLogger('').setFormatter(formatter)

    rootLogger = logging.getLogger('')
    rootLogger.addHandler(rFileHandler)
    if False:
        rootLogger.addHandler(GMailHandler())

if __name__ == '__main__':
    setup()
    #mirrorLogsToGMail()
    #logging.info('test-append')

