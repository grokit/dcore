
import xml.etree.ElementTree
import zipfile
import re
import datetime
import os
import argparse

_meta_shell_command = 'convert_docx'

def getArgs():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', type = str, help="File to convert.")
    args = parser.parse_args()

    return args

def _getFileContentFromZip(f, fileRegex):
    with zipfile.ZipFile(f) as zf:
        coreXml = [x for x in zf.namelist() if re.search(fileRegex, x) is not None]
        if len(coreXml) != 1:
            es = "Expect 1 core.xml, found %i: %s." % (len(coreXml), ", ".join(coreXml))
            raise Exception(es)
        coreXml = coreXml[0]
        
        with zf.open(coreXml) as myfile:
            return myfile.read().decode('utf-8')

def _getCoreContent(f):
    return _getFileContentFromZip(f, 'core\.xml$')

def parseDocxMainDocumentXMLAsMarkdown(docStr):
    root = xml.etree.ElementTree.fromstring(docStr)

    D = []
    it = root.iter() # 'body'
    for ele in it:
        #print(ele.tag)
        
        if re.search(r'}t', ele.tag) is not None:
            if ele.text is not None:
                D.append(ele.text)
        
        if re.search(r'}cNvPr', ele.tag) is not None:
            name = ele.attrib['name']
            D.append('![%s](%s)' % (name, name))
            
        if re.search(r'}p', ele.tag) is not None:
            D.append("\n")

    return "".join(D)

def parseDocxJuiceMedia(f):
    """
    Given a filename, return a list of tuples:
    [
    ('image1.jpg', b'<binary content>'),
    ('image2.jpg', b'<binary content>'),
    (...)
    ]
    """
    
    L = []
    with zipfile.ZipFile(f) as zf:
        imgs = [x for x in zf.namelist() if re.search('\.(jpg|png)', x) is not None]
        
        for img in imgs:
            with zf.open(img) as myfile:
                L.append((img, myfile.read()))
    return L
    
def getAsMarkdown(f):
    doc = _getFileContentFromZip(f, 'document\.xml$')
    #open('orig.xml', 'wb').write(doc.encode())
    md = parseDocxMainDocumentXMLAsMarkdown(doc)
    return md

def getCreatedAt(f):
    """
    Return in simple YYYY-MM-DD format.
    """
    
    core = _getCoreContent(f)
    dateStr = re.search(r'dcterms:created.*?>(.*?)<', core).group(1)
    # Parsing ISO: 2015-06-21T21:04:00Z
    # 2012-08-07T16:44:00.0000000Z 
    if len(dateStr.split('.')) == 2:
        assert dateStr.split('.')[1][-1] == 'Z'
        dateStr = dateStr.split('.')[0] + 'Z'
    date = datetime.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')
    return date.strftime("%Y-%m-%d") #?? this is localtime or UTC?

    
def filenameNoJunk(f, add = ''):
    a = "abcdefghijklmnopqrstuvwxyz0123456789-_[]" + add
    O = []
    for c in f:
        if c not in a:
            O.append('_')
        else:
            O.append(c)
    return "".join(O)
    
def ensure_dir(f):
    print('ensure',f)
    if not os.path.exists(f):
        os.makedirs(f)
        
def writeFinal(name, dateStr, md, media):
    folder = os.path.join(os.getcwd(), dateStr)
    ensure_dir(folder)
    
    fout = os.path.join(folder, "%s.md" % filenameNoJunk(name))
    print(fout)
    open(fout, 'wb').write(md.encode())

    # assert no duplicates
    #assert len(set(media)) == len(m)
    
    for m in media:
        if m == '':
            m = 'noname'
            
        fout = os.path.join(folder, filenameNoJunk(m[0], '.'))
        print(fout)
        open(fout, 'wb').write(m[1])
    
if __name__ == '__main__':
    args = getArgs()
    filename = args.file
    
    createdAt = getCreatedAt(filename)
    md = getAsMarkdown(filename)
    media = parseDocxJuiceMedia(filename)
    
    name = os.path.splitext(filename)[0]
    print(name)
    print(createdAt)
    writeFinal(name, createdAt, md, media)
