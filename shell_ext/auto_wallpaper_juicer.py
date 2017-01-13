
import dcore.data as data

import shutil
import os
import urllib.request
import logging
import time
import re
import random
import argparse

_meta_shell_command = 'getpics'

outputFolder = os.path.join(data.dcoreTempData(), 'wallpapers') 
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

linux_setpic_cmds = ['gsettings set org.gnome.desktop.background picture-uri file:///%s']
linux_setpic_cmds.append('feh --bg-scale %s')

class ScriptLogHandler(logging.FileHandler):

    """
    Save to file and output to screen.
    """

    def emit(self, record):
        print("{0}: {1}".format(record.levelname, record.getMessage()))
        logging.FileHandler.emit(self, record)


def forceToAscii(bytes):
    ascii = []
    for byte in bytes:
        if byte > 0 and byte < 128:
            ascii.append(chr(byte))
    return "".join(ascii)


def getHtmlAsText(url):
    sock = urllib.request.urlopen(url)
    url_bytes = sock.read()
    sock.close()

    url_txt = forceToAscii(url_bytes)

    return url_txt


def getUrlsFiles(html, regex):
    imgs = re.findall(regex, html, re.MULTILINE)
    return imgs

ALLOWEDCHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
def substIllegalCharsInFilename(filename):
    lstOutChars = []
    for char in filename:
        if char in ALLOWEDCHARS:
            lstOutChars.append(char)
        else:
            lstOutChars.append('_')
    str = "".join(lstOutChars)
    return str


def downloadAllUrls(urls):

    for url in urls:
        filename = outputFolder + "/" + substIllegalCharsInFilename(url)
        logger.debug("Fetching {0}, writing to: {1}".format(url, filename))
        try:
            sock = urllib.request.urlopen(url)
            url_bytes = sock.read()
            sock.close()

            fh = open(filename, 'wb')
            fh.write(url_bytes)
            fh.close()
        except:
            logger.debug("Error fetching file-url: {0}".format(url))


def saveUrlFetched(url, url_content):
    filename = outputFolder + "/" + substIllegalCharsInFilename(url).lower()
    file = open(filename, 'w')
    file.write(url_content)
    file.close()


def ripUrls(urls, regex):
    for url in urls:
        try:
            logger.debug("Try get website: {0}".format(url))
            html = getHtmlAsText(url)
            #saveUrlFetched(url, html)
            files_url = getUrlsFiles(html, regex)
            downloadAllUrls(files_url)
        except BaseException as e:
            logger.debug("Error fetching website: {0}".format(url))


def movePicsToOld():
    dir = outputFolder + '/old'

    if not os.path.isdir(dir):
        os.mkdir(dir)
    # shutil.rmtree(dir)

    files = os.listdir(outputFolder)
    images = [file for file in files if file.split('.')[-1].lower() == 'jpg']

    for file in images:
        src = outputFolder + '/' + file
        dst = dir + '/' + file
        shutil.move(src, dst)

def getArgs():
        
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--move_old', action = "store_true", default=True)
    parser.add_argument('-f', '--fetch_new', action = "store_true", default=True)
    parser.add_argument('-c', '--just_change_background', action = "store_true", default=False)

    args = parser.parse_args()

    if args.just_change_background is True:
        args.move_old = False
        args.fetch_new = False

    return args


if __name__ == '__main__':
    args = getArgs()

    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    log_handler = ScriptLogHandler(outputFolder + "/get_pics.log")
    log_handler.setLevel(logging.DEBUG)
    logger.addHandler(log_handler)

    if args.move_old is True:
        movePicsToOld()

    if args.fetch_new is True:
        urls = ['http://www.reddit.com/r/earthporn',
                'http://www.reddit.com/r/CityPorn',
                'http://www.reddit.com/r/VillagePorn',
                'http://www.reddit.com/r/InfrastructurePorn',
                'http://www.reddit.com/r/WaterPorn']

        regex = r"(http://i.imgur.com/.*?)\""

        ripUrls(urls, regex)

    pics = [
        os.path.join(
            outputFolder,
            f) for f in os.listdir(outputFolder) if re.search(
            r'\.jpg$',
            f) is not None]

    rI = random.randint(0, len(pics)-1)
    pic = pics[rI]
    for linux_setpic_cmd in linux_setpic_cmds:
        cmd = linux_setpic_cmd % pic
        os.system(cmd)
