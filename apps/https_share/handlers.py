
import os
import hashlib
import logging
import base64

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
    
    body = "<h2>File uploaded successfully.</h2><p>Filename: %s.<br>Len: %s.<br>MD5 hash: %s<br></p>"
    
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

