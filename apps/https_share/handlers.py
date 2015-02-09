
import os
import hashlib
import logging
import base64
import tempfile

import htmlt

log = logging.getLogger('log')

def base64AsStr(str):
    return base64.b64encode(str.encode()).decode('ascii')

def getHash(content):
    m = hashlib.md5()
    m.update(content)
    return m.hexdigest()

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

def getStyle():
    
    css_file = os.path.join( os.path.dirname(os.path.realpath(__file__)), 'flask_style.css')
    
    fh = open(css_file, 'r')
    cnt = fh.read()
    return cnt

def getHtmlDebugInfo(httpHanlder):
    
    lHeaders = []
    for k, v in httpHanlder.headers.items():
        lHeaders.append("%s: %s<br>" % (k, v))
    
    debug_mid = "<br><br><br><br><p><b>Debug Information</b><br>%s<br>%s<br>%s<br></p>" % (httpHanlder.command, httpHanlder.path, "".join(lHeaders))
    
    return '<div class="debug_info">%s</div>' % debug_mid    

def extractHeadersInfo(listFileHandles):
    """
    Example:
    ^M
    ------WebKitFormBoundaryZ9iJ45MfUXz8jMs2^M
    Content-Disposition: form-data; name="uploadedfile"; filename="http___i.imgur.com_1TkfgMv.jpg"
    Content-Type: image/jpeg
    
    [... file content ...]

    See: http://www.w3.org/Protocols/rfc1341/7_2_Multipart.html
    """

    log.debug(locals())
    
    firstFh = listFileHandles[0]
    firstFh.seek(0)
    multipart = firstFh.read()
    header, data = multipart.split(b'\r\n\r\n', 1)
    header = header + b'\r\n\r\n'
    
    log.debug(header)
    
    boundaryTag = b'\r\n' + header.split(b'\r\n')[0]
    filename = header.split(b'filename="')[1].split(b'"')[0]
    filename = filename.decode('ascii')
    
    log.debug('Detected boundary: %s.' % boundaryTag)

    dataStartPos = len(header)
    
    return filename, boundaryTag, dataStartPos 

def writeMultipartFile(listFileHandlers, filenameOut, dataStartPos, boundaryTag):

    fh = open(filenameOut, 'wb')

    for i, fht in enumerate(listFileHandlers):
        log.debug('Write non-temp chunk %i of %i.' % (i, len(listFileHandlers)))
        fht.seek(0)

        done = False
        while not done:
            readD = fht.read(2**20)
            log.debug('Read from temp file %i byte(s).' % len(readD))

            if i == 0:
                readD = readD[dataStartPos:]

            # @@bug what happens if the boundary is split between two chunks?
            posF = readD.find(boundaryTag)
            if posF != -1:
                log.debug('Found boundary at pos %i.' % posF)
                readD = readD[0:posF]
                done = True

            fh.write(readD)

            if len(readD) == 0:
                #raise Exception("Should end with boundary -- file is most likely corrupted.")
                done = True
    fh.close()
    log.debug('Done writeMultipartFile.')

def handleUploadSink(httpHandler):
    
    if httpHandler.headers['content-length'] is None:
        handleCustomError(httpHandler, "No 'content-length' header, browser is not trying to upload?")
        return
    
    length = int(httpHandler.headers['content-length'])
    
    log.debug(httpHandler.headers)
    outputFolder = httpHandler.server.data['output_folder']
    log.debug('File upload output folder: %s.' % outputFolder)

    Lfh = []
    lenRecv = 0
    log.debug('Starting upload read...')
    while True:
        fh = tempfile.TemporaryFile()
        Lfh.append(fh)
        
        log.debug('Reading chunk %i.' % len(Lfh))

        readLen = 2**20
        if readLen > length-lenRecv:
            readLen = length-lenRecv

        log.debug('Attempt read %i byte(s).' % readLen)
        data = httpHandler.rfile.read(readLen)
        log.debug('Read %i byte(s).' % len(data))
        lenRecv += len(data)
        fh.write(data)
        
        if len(data) == 0 or lenRecv == length:
            break
    
    # This write the files in temp files, then merge to final file. Thus it writes everything twice. A better implementation would
    # write to a single file, and detect / correct MIME heads on the fly using the two latest chunks read.
    filename, boundaryTag, dataStartPos = extractHeadersInfo(Lfh)
    filename = 'recv_' + filename # Avoid letting the client completely set the filename -- could override arbitrary files including scripts.
    fullpath = os.path.join(outputFolder, filename)
    log.debug('File upload output filename: %s.' % fullpath)
    writeMultipartFile(Lfh, fullpath, dataStartPos, boundaryTag)

    httpHandler.send_response(200)
    httpHandler.send_header('Content-type','text/html')
    httpHandler.end_headers()
    
    body = "<h2>File uploaded successfully.</h2><p>Filename: %s.<br>Len: %s.<br>MD5 hash: %s<br></p>"
    
    html = htmlt.html_template
    html = html.replace('__head__', '')
    html = html.replace('__style__', getStyle())
    html = html.replace('__body__', body % (filename, len(data), 'hash computation skipped'))
    html = html.replace('__debug_info__', getHtmlDebugInfo(httpHandler))
    
    httpHandler.wfile.write(html.encode())

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
    html = html.replace('__body__', htmlt.upload_body)
    html = html.replace('__debug_info__', getHtmlDebugInfo(httpHanlder))
    
    httpHanlder.wfile.write(html.encode())

