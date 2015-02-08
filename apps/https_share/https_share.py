#!/usr/bin/python3

"""
# TODO

- This is messy, split in files
    - html
    - handlers

- COMPLEX: break-down functionalities in modules that embed and isolate their complexity.

- Ping localhost (or broadcast or UDP dns, ...), not google to get local IP.

- Have an HTTP interface when you can just POST a file and it gets swallowed to a file.

# Bugs

- When uploading, limited by size of memory because the current MIME-chunk implementation relies on having the whole file.
- When using a custom folder, the uploads will not automatically go there.

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
import base64
import logging
import traceback

from urllib.parse import urlparse
from random import randint

import htmlt

_meta_shell_command = 'https_share'

def pickRandomToken(pre):
    rBytes = os.urandom(8*1024)
    return pre + hashlib.sha224(rBytes).hexdigest()
    
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

def getHtmlDebugInfo(httpHanlder):
    
    lHeaders = []
    for k, v in httpHanlder.headers.items():
        lHeaders.append("%s: %s<br>" % (k, v))
    
    debug_mid = "<br><br><br><br><p><b>Debug Information</b><br>%s<br>%s<br>%s<br></p>" % (httpHanlder.command, httpHanlder.path, "".join(lHeaders))
    
    return '<div class="debug_info">%s</div>' % debug_mid    
    
def getHtmlDir(path):
    
    lHtml = []
    try:
        files = os.listdir(path)
        
        lHtml.append("<h2>Files</h2>")
        
        subFolder = os.path.abspath( os.path.join(path, "./..") )
        subFolderFriendly = os.path.abspath( os.path.join(path, ".") ) + '/..'
        
        lHtml.append('Parent: <a href="query=%s">%s</a><br>' % (base64AsStr(subFolder), subFolderFriendly))
        
        for file in files:
            lHtml.append('<a href="query=%s">%s</a><br>' % (base64AsStr(os.path.join(path, file)), file))
        
    except BaseException as e:
        lHtml.append('Path not found: %s.<br>' % path)
        eStr = "%s" % e
        eStr = eStr.replace("\n", "<br>")
        lHtml.append(eStr)
        log.error(eStr)
        
    return "\n".join(lHtml)
        
def isPathAuthorized(authorizedFolder, queryFolder):
    
    authorizedFolder = os.path.realpath(authorizedFolder)
    queryFolder = os.path.realpath(queryFolder)
    
    last = queryFolder
    while(True):

        if queryFolder == authorizedFolder:
            return True
        
        queryFolder = os.path.realpath( os.path.join(queryFolder, '..') )
        
        if queryFolder == last:
            return False
        
        last = queryFolder
    
    return False
    
def handleUrlListFiles(httpHanlder):
    
    queryPath = httpHanlder.server.data['authorized_folder']
    
    if "query=" in httpHanlder.path:
        queryPath = httpHanlder.path.split("query=")[1]
        
        if type(queryPath) != type(b''):
            queryPath = queryPath.encode()        
        
        queryPath = base64.b64decode(queryPath)
        
        if type(queryPath) == type(b''):
            queryPath = queryPath.decode()
        
        log.debug("queryPath: %s" % queryPath)
    
    if not isPathAuthorized(httpHanlder.server.data['authorized_folder'], queryPath):
        handleNotAuthorizedFolder(httpHanlder, queryPath)
        return
    
    if os.path.isdir(queryPath):
        httpHanlder.send_response(200)
        httpHanlder.send_header('Content-type','text/html')
        httpHanlder.end_headers()
        
        html = htmlt.html_template
        html = html.replace('__head__', '')
        html = html.replace('__style__', getStyle())
        html = html.replace('__body__', getHtmlDir(queryPath))
        html = html.replace('__debug_info__', getHtmlDebugInfo(httpHanlder))
        
        httpHanlder.wfile.write(html.encode())
        
    elif os.path.isfile(queryPath):
        
        filename = os.path.split(queryPath)[1]
        
        httpHanlder.send_response(200)
        httpHanlder.send_header('Content-disposition','attachment; filename=%s' % filename)
        httpHanlder.end_headers()

        fh = open(queryPath, 'rb')
        chunkSize = 1024*32
        while True:
            fileBytes = fh.read(chunkSize)
            if len(fileBytes) == 0:
                break
            httpHanlder.wfile.write(fileBytes)
        fh.close()

    else:
        handleNotFound(httpHanlder)

def getStyle():
    
    css_file = os.path.join( os.path.dirname(os.path.realpath(__file__)), 'flask_style.css')
    
    fh = open(css_file, 'r')
    cnt = fh.read()
    return cnt

def handleMain(httpHanlder):
    
    httpHanlder.send_response(200)
    httpHanlder.send_header('Content-type','text/html')
    httpHanlder.end_headers()
    
    html = htmlt.html_template
    html = html.replace('__head__', '')
    html = html.replace('__style__', getStyle())
    html = html.replace('__body__', htmlt.main_html)
    html = html.replace('__debug_info__', getHtmlDebugInfo(httpHanlder))
    
    httpHanlder.wfile.write(html.encode())
       
def handleLog(httpHanlder):
    
    httpHanlder.send_response(200)
    httpHanlder.send_header('Content-type','text/html')
    httpHanlder.end_headers()
    
    fh = open(logfilename, 'r')
    logCt = fh.read()
    fh.close()
    
    html = htmlt.html_template
    html = html.replace('__head__', '')
    html = html.replace('__style__', getStyle())
    html = html.replace('__body__', htmlt.main_log.format( logCt ))
    html = html.replace('__debug_info__', getHtmlDebugInfo(httpHanlder))
    
    httpHanlder.wfile.write(html.encode())

def handleCustomError(httpHanlder, errMsg):
    
    errNo = 400
    
    httpHanlder.send_response(errNo)
    httpHanlder.send_header('Content-type','text/html')
    httpHanlder.end_headers()
    
    html = htmlt.html_template
    html = html.replace('__head__', '')
    html = html.replace('__style__', getStyle())
    html = html.replace('__body__', r'<h2>%s Bad Request, %s</h2>' % (errNo, errMsg))
    html = html.replace('__debug_info__', getHtmlDebugInfo(httpHanlder))
    
    httpHanlder.wfile.write(html.encode())

    
def handleNotFound(httpHanlder):
    
    httpHanlder.send_response(404)
    httpHanlder.send_header('Content-type','text/html')
    httpHanlder.end_headers()
    
    html = htmlt.html_template
    html = html.replace('__head__', '')
    html = html.replace('__style__', getStyle())
    html = html.replace('__body__', r'<h2>404 Not Found :(</h2>')
    html = html.replace('__debug_info__', getHtmlDebugInfo(httpHanlder))
    
    httpHanlder.wfile.write(html.encode())

def handleNotAuthorizedFolder(httpHanlder, resource):
    
    httpHanlder.send_response(401)
    httpHanlder.send_header('Content-type','text/html')
    httpHanlder.end_headers()
    
    html = htmlt.html_template
    html = html.replace('__head__', '')
    html = html.replace('__style__', getStyle())
    html = html.replace('__body__', htmlt.not_auth_folder_body)
    html = html.replace('__resource__', os.path.realpath( resource ) )    
    html = html.replace('__debug_info__', getHtmlDebugInfo(httpHanlder))
    
    httpHanlder.wfile.write(html.encode())    

def handleNotAuthorized(httpHanlder):
    
    httpHanlder.send_response(401)
    httpHanlder.send_header('Content-type','text/html')
    httpHanlder.end_headers()
    
    html = htmlt.html_template
    html = html.replace('__head__', '')
    html = html.replace('__style__', getStyle())
    html = html.replace('__body__', htmlt.not_auth_body)
    html = html.replace('__debug_info__', getHtmlDebugInfo(httpHanlder))
    
    httpHanlder.wfile.write(html.encode())    

    
def handleUpload(httpHanlder):
    
    httpHanlder.send_response(200)
    httpHanlder.send_header('Content-type','text/html')
    httpHanlder.end_headers()
    
    html = htmlt.html_template
    html = html.replace('__head__', '')
    html = html.replace('__style__', getStyle())
    html = html.replace('__body__', html.upload_body)
    html = html.replace('__debug_info__', getHtmlDebugInfo(httpHanlder))
    
    httpHanlder.wfile.write(html.encode())
    
def getHash(content):
    m = hashlib.md5()
    m.update(content)
    return m.hexdigest()
    
def coonvertMultipartToFile(multiplart):
    """
    Example:
    ^M
    ------WebKitFormBoundaryZ9iJ45MfUXz8jMs2^M
    Content-Disposition: form-data; name="uploadedfile"; filename="http___i.imgur.com_1TkfgMv.jpg"
    Content-Type: image/jpeg
    
    [... file content ...]
    """
    
    log.debug(type(multiplart))
    header, data = multiplart.split(b'\r\n\r\n', 1)
    
    log.debug(header)
    
    boundary = header.split(b'\r\n')[0]
    filename = header.split(b'filename="')[1].split(b'"')[0]
    filename = filename.decode('ascii')
    
    log.debug('Detected boundary: %s.' % boundary.decode())
    
    data = data.split(b'\r\n' + boundary + b'--')[0] #\r\n
    
    hashV = getHash(data)
    
    return (filename, data, hashV)
    
def handleUploadSink(httpHanlder):
    
    if httpHanlder.headers['content-length'] is None:
        handleCustomError(httpHanlder, "No 'content-length' header, browser is not trying to upload?")
        return
    
    length = int(httpHanlder.headers['content-length'])
    
    filename = 'upload'
    log.debug(httpHanlder.headers)
    
    lD = []
    MB = 2**20
    lenRecv = 0
    while True:
        
        cLen = length - lenRecv
        
        if cLen > MB:
            cLen = MB
            
        data = httpHanlder.rfile.read(cLen)
        lenRecv += len(data)
        
        lD.append( data )
        
        if len(data) == 0 or lenRecv == length:
            break
    
    data = b"".join(lD)
    
    filename, data, hashV = coonvertMultipartToFile(data)
    
    fullpath = os.path.join(httpHanlder.server.data['output_folder'], filename)
    
    with open(fullpath, 'wb') as fh:
        log.debug('Got upload: %s, %s bytes. Written to: %s.' % (filename, length, fullpath))
        fh.write(data)

    httpHanlder.send_response(200)
    httpHanlder.send_header('Content-type','text/html')
    httpHanlder.end_headers()
    
    body = "<h2>File uploaded successfully.</h2><p>Filename: %s.<br>Len: %s.<br>Hash: %s<br></p>"
    
    html = htmlt.html_template
    html = html.replace('__head__', '')
    html = html.replace('__style__', getStyle())
    html = html.replace('__body__', body % (filename, len(data), hashV))
    html = html.replace('__debug_info__', getHtmlDebugInfo(httpHanlder))
    
    httpHanlder.wfile.write(html.encode())

def handleSetToken(httpHanlder):
    
    tokenV = httpHanlder.path.split("/")[-1]
    
    if tokenV[0] == '?':
        tokenV = tokenV.split('?accessToken=')[1]
    
    httpHanlder.send_response(200)
    httpHanlder.send_header('Content-type','text/html')
    httpHanlder.send_header('Set-Cookie', 'accessToken=%s;Path=/; HttpOnly' % tokenV)
    httpHanlder.end_headers()
    
    html = htmlt.html_template
    html = html.replace('__head__', '<meta http-equiv="refresh" content="3;url=/" />')
    html = html.replace('__style__', getStyle())
    html = html.replace('__body__', r'<p><b>Token set to: %s.</b></p>You will be redirected automatically.' % tokenV)
    html = html.replace('__debug_info__', getHtmlDebugInfo(httpHanlder))
    
    httpHanlder.wfile.write(html.encode())
    
def base64AsStr(str):
    return base64.b64encode(str.encode()).decode('ascii')
    
def functorFromUrl(url):
    
    hDict = {}
    hDict[r'^/$'] = handleMain
    hDict[r'^/log/$'] = handleLog
    hDict[r'^/upload/sink/$'] = handleUploadSink
    hDict[r'^/upload/$'] = handleUpload
    hDict[r'^/files/.*'] = handleUrlListFiles
    
    for k, v in hDict.items():
        if re.search(k, url):
            return v
    
    return None

def isAuthorized(httpHanlder):
        tokenV = ''
        cookies = httpHanlder.headers.get('Cookie')
        if cookies and len(cookies.split('accessToken=')) > 0:
            tokenV = cookies.split('accessToken=')[1]
        
        if tokenV == httpHanlder.server.data['access_token']:
            return True
        
        return False

class AddDataTCPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, data = None):
        self.data = data
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)

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
                handleNotAuthorized(self)
                return
            
            if fn is not None:
                fn(self)
            else:
                handleNotFound(self)
        
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error("".join(traceback.format_exception(exc_type, exc_value,exc_traceback)))
    
    def do_GET(self):
        try:
            fn = functorFromUrl(self.path)
            
            # Bypass authorization for set cookie url
            if re.search('^/set_cookie/.*', self.path):
                handleSetToken(self)
                return
            
            if not isAuthorized(self):
                handleNotAuthorized(self)
                return
            
            if fn is not None:
                fn(self)
            else:
                handleNotFound(self)
        
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error("".join(traceback.format_exception(exc_type, exc_value,exc_traceback)))

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
    log = logging.getLogger('log')
    logging.getLogger("log").addHandler(PrintHandler())
    
    log.info(args)
    
    ip = '0.0.0.0'
    
    server_address = (ip, args.port)
    
    dataToServer = {'access_token': args.access_token, 'authorized_folder': args.share_root_directory, 'output_folder': args.output_folder}
    httpd = AddDataTCPServer(server_address, CustomHTTPHandler, data=dataToServer)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                server_side=True,
                                certfile=args.cert_file)
    
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
    
