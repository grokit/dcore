
import os
import logging
import datetime

from logging.handlers import TimedRotatingFileHandler

import dcore.data as data
import dcore.apps.gmail.gmail as gmail
import dcore.private_data as private_data

def dateForAnnotation():
    return datetime.datetime.now().isoformat()

class GMailHandler(logging.Handler):

    def emit(self, record):
        title = "GMail Handler m3pzBxlKu %s" % dateForAnnotation()
        msg = self.format(record)
        gmail.sendEmail(private_data.primary_email, title, msg)

def setup():
    logging.basicConfig(level=logging.DEBUG)
    folder = data.dcoreTempData() + '/logs'
    data.createDirIfNotExist(folder)
    print(folder)
    logFilename = os.path.join(folder, 'dcore.log')
    rFileHandler = TimedRotatingFileHandler(logFilename, when='S')
    rootLogger = logging.getLogger('')
    rootLogger.addHandler(rFileHandler)
    rootLogger.addHandler(GMailHandler())

if __name__ == '__main__':
    # TODO: setup gmail as additional handler: setupAddGmail()
    setup()
    logging.info('hello')

