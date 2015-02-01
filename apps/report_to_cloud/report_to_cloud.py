"""
# TODO
- Eliminate the port magic requirement.
- Remove unused imports.
"""

import sys
import os
import argparse
import socket
import json
import time
import threading
import urllib
import urllib.request
import http.client
import urllib.parse
import platform
import time
import logging

_meta_shell_command = 'report_to_cloud'

logfilename = os.path.join('.', '%s.log' % __file__.replace('.py', ''))
UpdateIntervalInSecs = 90

class PrintHandler(logging.Handler):
    def emit(self, record):
        rtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))
        print(record.getMessage())

class DictToClass:
    
    def __init__(self, inDict): 
        self.__dict__ = inDict
    
    def __str__(self):
        return str(self.__dict__)

def getLocalIP():
    # Would work as well?: print(socket.gethostbyname(socket.gethostname()))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("www.google.com", 80))
    ip = s.getsockname()[0]
    s.close()
    
    return ip

def getPublicIP():
    ip = str(urllib.request.urlopen('http://ip.42.pl/raw').read(), "utf8")
    return ip

def threadLoopUpdateToCloud(userName, serverIPPort, starter = True):
    
    if starter == True:
        t = threading.Thread(target = threadLoopUpdateToCloud, args = ([userName, serverIPPort, False]))
        t.daemon = False # Process will wait for thread end for exit.
        t.start()
    else:
        lastUpdated = 0
        checkInterval = 30
        
        try:
            userIP = getLocalIP()
            userIPPublic = getPublicIP()
            uploadUserInfoToCloud(userName, userIP, userIPPublic, serverIPPort)
        except BaseException as e:
            log.error("Exception: %s." % e)
            time.sleep(checkInterval)
            
        while True:
            
            try:
                userIP = getLocalIP()
                
                if userIP != getLocalIP():
                    uploadUserInfoToCloud(userName, userIP, userIPPublic, serverIPPort)
                
                lastUpdated += checkInterval
                time.sleep(checkInterval)
                
                if lastUpdated >= UpdateIntervalInSecs:
                    lastUpdated = 0
                    uploadUserInfoToCloud(userName, userIP, userIPPublic, serverIPPort)
            
            except BaseException as e:
                log.error("Exception: %s." % e)
                time.sleep(checkInterval)
                
def getArgs():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-s', '--server', default = 'incomingp2p.appspot.com:80')
    parser.add_argument('-l', '--localhost_server', action = 'store_true')

    args = parser.parse_args()

    if args.server.find(':') == -1: args.server = args.server + ':80'
    if args.localhost_server == True: args.server = '127.0.0.1:8080'

    return args

def uploadUserInfoToCloud(userName, userIP, userIPPublic, serverIPPort):
    
    #@@todo: just receive JSON here, do not do any processing on input
    serverIP = serverIPPort[0]
    serverPort = serverIPPort[1]
    
    postBody = json.dumps({'publicIP': userIPPublic, 'version':'2', 'name': userName, 'localIP': userIP})
    
    log.debug("uploadUserInfoToCloud: %s." % postBody)

    headers = {'User-agent': 'dp2p'}
    conn = http.client.HTTPConnection(serverIP, serverPort)
    conn.request("POST", "/share_ip", postBody, headers)
    response = conn.getresponse()
    
    data = response.read()
    conn.close()
    
    if response.status != 200 or response.reason != 'OK':
        log.debug(data)
        raise Exception("Invalid reply.")
    
def downloadUserInfoFromCloud(serverIPCache):
    
    headers = {'User-agent': 'dp2p'}
    conn = http.client.HTTPConnection(serverIPCache[0], serverIPCache[1])
    conn.request("GET", "/share_ip", '', headers)
    response = conn.getresponse()
    
    data = response.read().decode()
    conn.close()
    
    if response.status != 200 or response.reason != 'OK':
        log.debug(data)
        raise Exception("Invalid reply.")
    
    dJson = json.loads( data )
    
    log.debug(dJson)
    
    remDupl = {}
    for dUser in dJson:
        remDupl[dUser['name']] = dUser
    
    lUsers = []
    dbgSb = []
    for (k, v) in remDupl.items():
        u = DictToClass(v)
        lUsers.append(u)
        dbgSb.append(str(u))
    
    log.debug('downloadUserInfoFromCloud(): users from cloud: %s.' % " ".join(dbgSb))
    
    return lUsers

def getLocalUsername():
    return  platform.node()
 
if __name__ == '__main__':
     
    logging.basicConfig(format='%(levelname)s %(asctime)-15s %(message)s', filename = logfilename, level=logging.DEBUG, datefmt='%Y-%m-%d_%H:%M_%Ss')
    log = logging.getLogger('log')
    logging.getLogger("log").addHandler(PrintHandler())

    args = getArgs()
    log.debug(args)
  
    serverIPCache = args.server.split(':')

    threadLoopUpdateToCloud(getLocalUsername(), serverIPCache)
    usersInfo = downloadUserInfoFromCloud(serverIPCache)
    log.debug(usersInfo)
    
