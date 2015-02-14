#!/usr/bin/python3

"""
# TODO

## As

- File UPLOAD (1.4GB) sometimes MD5 sum does not match.

## Bs

- OSError: [Errno 24] Too many open files: '/tmp/tmp8oum1l' <-- chunking with hundreds of open filehandles is not a good idea apparently.
    - Only affect very large (10GB+) files.

- COMPLEX: break-down functionalities in modules that embed and isolate their complexity.

- Have an HTTP interface when you can just POST a file and it gets swallowed to a file.

- Pivot: maybe this project could be a 'web read-write'? Provide a way to store data in the web if you provide the nodes?

# Bugs

- Uploading could corrupt file: compute md5 and check boundary using latest 2 chunks, not 1.
- The IP in the link is sometimes not the public IP.

# Notes

- http://pymotw.com/2/BaseHTTPServer/, https://docs.python.org/3.4/library/socketserver.html

"""

_meta_shell_command = 'https_share'

import hashlib
import signal
import re
import argparse
import socket
import sys
import os
import http.client
import http.server
import ssl
import webbrowser
import socketserver
import time
import urllib.request
import logging
import traceback

from urllib.parse import urlparse
from random import randint

import htmlt
import handlers

def getArgs():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-a', '--access_token', type = str, default = pickRandomToken('randomToken_'), help = 'You need to have this token in order to be able to access the https website.')
    parser.add_argument('-p', '--port', type = int, default = 4443)
    parser.add_argument('-s', '--share_root_directory', default = '.', type = str, help = 'You share everything in that folder and all sub-folders.')
    parser.add_argument('-c', '--cert_file', type = str, default = None)
    parser.add_argument('-o', '--output_folder', default = '.', type = str, help = 'Where the logs / uploaded files go.')
    
    args = parser.parse_args()
    
    args.share_root_directory = os.path.realpath( args.share_root_directory )
    
    if not os.path.isdir( args.share_root_directory ):
        raise BaseException("Invalid directory for args.share_root_directory: %s." % args.share_root_directory)
    
    if args.cert_file is None:
        args.cert_file = os.path.join( os.path.dirname(os.path.realpath(__file__)), 'default_server_cert.pem')
    
    return args

class PrintHandler(logging.Handler):
    def emit(self, record):
        rtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))
        print(record.getMessage())

def pickRandomToken(pre):
    rBytes = os.urandom(8*1024)
    return pre + hashlib.sha224(rBytes).hexdigest()
    
def functorFromUrl(url):
    
    hDict = {}
    hDict[r'^/$'] = handlers.handleMain
    hDict[r'^/log/$'] = handlers.handleLog
    hDict[r'^/upload/sink/$'] = handlers.handleUploadSink
    hDict[r'^/upload/$'] = handlers.handleUpload
    hDict[r'^/files/.*'] = handlers.handleUrlListFiles
    
    for k, v in hDict.items():
        if re.search(k, url):
            return v
    
    return None

def isAuthorized(httpHanlder):
    tokenV = ''
    cookies = httpHanlder.headers.get('Cookie')
    if cookies and len(cookies.split('accessToken=')) > 0:
        log.debug('Cookies: %s.' % cookies)
        tokenV = cookies.split('accessToken=')[1]
    
    if tokenV == httpHanlder.server.data['access_token']:
        return True
    
    return False

class CustomHTTPHandler(http.server.BaseHTTPRequestHandler):
    
    def serve_forever(self):
        self.stop = False
        while not self.stop:
            self.handle_request()    
        log.debug('serve_forever ended')
    
    def do_POST(self):
        
        #@@refactor to use same code as GET
        
        try:
            fn = functorFromUrl(self.path)
            
            if not isAuthorized(self):
                handlers.handleNotAuthorized(self)
                return
            
            if fn is not None:
                fn(self)
            else:
                handlers.handleNotFound(self)
        
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error("".join(traceback.format_exception(exc_type, exc_value,exc_traceback)))
    
    def do_GET(self):
        try:
            fn = functorFromUrl(self.path)
            
            # Bypass authorization for set cookie url
            if re.search('^/set_cookie/.*', self.path):
                handlers.handleSetToken(self)
                return
            
            if not isAuthorized(self):
                handlers.handleNotAuthorized(self)
                return
            
            if fn is not None:
                fn(self)
            else:
                handlers.handleNotFound(self)
        
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error("".join(traceback.format_exception(exc_type, exc_value,exc_traceback)))

class AddDataTCPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, data = None):
        self.data = data
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)

class ThreadedHTTPServer(socketserver.ThreadingMixIn, AddDataTCPServer):
        """Handle requests in a separate thread."""

class SignalHandler:
    
    def signal_handler(self, signal, frame):
        log.debug('You pressed Ctrl+C, closing socket listener.')
        self.server.stop = True
        log.debug('Socket listener closed.')
        time.sleep(1)
        sys.exit(0)
        
def getMyIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com", 80))
    myIP = s.getsockname()[0]
    s.close()
    
    return myIP

if __name__ == '__main__':
    
    args = getArgs()
    
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)
    
    logfilename = args.output_folder + '/https_share.log'
    logging.basicConfig(format='%(levelname)s %(asctime)-15s %(message)s', filename = logfilename, level=logging.DEBUG, datefmt='%Y-%m-%d_%H:%M_%Ss')
    logging.getLogger("log").addHandler(PrintHandler())
    log = logging.getLogger('log')
    
    log.info(args)
    
    server_address = ('0.0.0.0', args.port)
    dataToServer = {'access_token': args.access_token, 'authorized_folder': args.share_root_directory, 'output_folder': args.output_folder}
    httpd = ThreadedHTTPServer(server_address, CustomHTTPHandler, data=dataToServer)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile=args.cert_file)
    
    sh = SignalHandler()
    sh.server = httpd
    signal.signal(signal.SIGINT, sh.signal_handler)
   
    myIp = getMyIP()
    
    link = "https://%s:%s/" % (myIp, args.port)
    linkPw = link + 'set_cookie/%s' % args.access_token
    
    log.info("Server starting at %s, have fun!" % (link))
    log.info("You can use this share link: %s" % linkPw)
    
    webbrowser.open_new_tab(linkPw)
    httpd.serve_forever()
        
    sys.exit(0)
    
