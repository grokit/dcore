#!/usr/bin/python3

"""
# TODO
- Store downloaded podcasts as JSON with date downloaded.
"""

import os
import os.path
import logging
import time
import re
import urllib.request
import random
import sys
import argparse

_meta_shell_command = 'podcasts'

folder_out = os.path.expanduser('~/Desktop/podcasts/')
#folder_out = os.path.split( __file__ )[0]
logfilename = os.path.join(folder_out, "podcasts.log")
downloadedDB = os.path.join(folder_out, "downloadedDB.log")

class PrintHandler(logging.Handler):
    def emit(self, record):
        rtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))
        print("{0}({1}): {2}".format(record.levelname, rtime, record.getMessage()))
        
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
        
ensure_dir(folder_out)
logging.basicConfig(format='%(levelname)s %(asctime)-15s %(message)s', filename = logfilename, level=logging.INFO, datefmt='%Y-%m-%d_%H:%M_%Ss')
log = logging.getLogger('log')
logging.getLogger("log").addHandler(PrintHandler())  

def appendDownloadedFiles(url):
    
    fh = open(downloadedDB, 'a')
    fh.write(url + '\n')
    fh.close()

def writeDownloadedFiles(htDl):
    
    fh = open(downloadedDB, 'w')
    
    for (k, v) in htDl.items():
        fh.write(k + '\n')
    
    fh.close()

def findPreviouslyDownloaded():
    
    if not os.path.isfile(downloadedDB):
        return {}
    
    fh = open(downloadedDB, 'r')
    lines = fh.readlines()
    fh.close()
    
    htFiles = {}
    for line in lines:
        
        htFiles[line.strip('\n')] = True
    
    return htFiles        

def downloadUrl(url, filename):
        
    if os.path.isfile(filename):
        #log.warning()
        raise Exception("File: {0}, already in directory.".format(filename))
    
    log.info("Fetching {0}, writing to: {1}".format(url, filename))
    
    #sock =  urllib.request.urlopen(url)
    #mp3_bytes = sock.read()
    #sock.close()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    mp3_bytes = urllib.request.urlopen(req).read()

    fh = open(filename, 'wb')
    fh.write(mp3_bytes)
    fh.close()

def substIllegalCharsInFilename(filename):
  allowedChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
  
  lstOutChars = []
  for char in filename:
    if char in allowedChars:
      lstOutChars.append(char)
    else:
      lstOutChars.append('_')
  return "".join(lstOutChars)

def downloadUrlsFromRSS(rssUrl):
    
    log.debug('downloadUrlsFromRSS %s' % rssUrl)
    
    urls = []
    
    # Workaround since a lot of website block python's user agent.
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    rss_content = urllib.request.urlopen(req).read()
    rss_content = rss_content.decode('UTF-8')

    for line in rss_content.splitlines():
        
        #print(line)        
        #m = re.search('(http://[^"]*?mp3)', line)
        m = re.search('(http://[^"]*?\.mp3)', line)
        
        if m is not None:
            urls.append(m.group(0))
    
    for durl in urls:
        log.debug('Juiced: %s.' % durl)
    
    return urls
    
def getArgs():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i', '--init', action = "store_true")
    
    args = parser.parse_args()
    
    return args

if __name__ == '__main__':
    
    log.debug('Podcasts start')
    
    args = getArgs()
    
    rssUrls = []
    rssUrls.append('http://www.economist.com/podcast/itunes/All%20audio')
    rssUrls.append('http://downloads.bbc.co.uk/podcasts/radio4/analysis/rss.xml')
    rssUrls.append('http://downloads.bbc.co.uk/podcasts/worldservice/docarchive/rss.xml')
    rssUrls.append('http://downloads.bbc.co.uk/podcasts/worldservice/whyfactor/rss.xml')
    rssUrls.append('http://feeds.thisamericanlife.org/talpodcast')
    rssUrls.append('http://feeds.wnyc.org/radiolab')

    # Wait wait, don't tell me
    rssUrls.append('http://www.npr.org/rss/podcast.php?id=344098539') 

    # All songs considered: http://www.npr.org/podcasts/510019/all-songs-considered 
    rssUrls.append('http://www.npr.org/templates/rss/podcast.php?id=510019') 

    #rssUrls.append('http://www.npr.org/templates/rss/podlayer.php?id=1017') # NPR business
    #rssUrls.append('http://www.npr.org/templates/rss/podlayer.php?id=1006') # NPR economy
    
    allDownloadUrls = []
    for url in rssUrls:
        
        downloadUrls = []
        try:
            downloadUrls = downloadUrlsFromRSS(url)
        except:
            log.warning('Failed to pull rss: %s.' % url)
        
        for durl in downloadUrls:
            allDownloadUrls.append(durl)
    
    random.shuffle(allDownloadUrls)
    
    if args.init is True:
        
        for url in allDownloadUrls:
            log.debug("Init mode: mark '%s' as already downloaded." % url)
            appendDownloadedFiles(url)
        
        sys.exit(0)
    
    for url in allDownloadUrls:
        
        pre = url.split('/')[-1].split('.')[0]
        #toFile = folder_out + pre + '_' + time.strftime("%Y-%m-%d_", time.localtime()) + substIllegalCharsInFilename(url)
        toFile = folder_out + pre + '.' + url.split('.')[-1]        
        #toFile = toFile.replace('_mp3', '.mp3')        
        
        htFiles = findPreviouslyDownloaded()
        
        if htFiles.get(url) is None:
            try:
                downloadUrl(url, toFile)
                appendDownloadedFiles(url)
            except Exception as e:
                log.warning('Failed to download %s. Except: %s.' % (url, e))
        else:
            log.debug('Skipping already downloaded %s.' % url)
    
    # Eliminate duplicates
    htFiles = findPreviouslyDownloaded()
    writeDownloadedFiles(htFiles)
    
    log.debug('Podcasts end')

