"""

Get created at from .docx:
https://github.com/python-openxml/python-docx

    >>> document = Document()
    >>> core_properties = document.core_properties
    >>> core_properties.author
    'python-docx'
    >>> core_properties.author = 'Brian'
    >>> core_properties.author
    'Brian'
    ------------------>
    created (datetime)
    Date of creation of the resource. (Dublin Core)

Get jpg 'took picture at':
https://pypi.python.org/pypi/ExifRead
^^ alternative is from filename if camera is cool

"""

import os
import re
import base64
import random

def createFolderIfNotExist(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def guessImageExt(imageBytes):
    # 4A 46 49 46 00 = "JFIF" in ASCII, terminated by a null byte, see  https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format
    if re.search(b'\x4a\x46\x49\x46\x00', imageBytes) is not None:
        return 'jpg'
    
    return 'png'
    
def markdownFix(filename, folderName):
    """
    Markdown converter inserts in-line images.
    This corrects the markdown file so that the images are converted from in-line:
    
            ![](data:image/*;base64,/9j/4AAQSkZJRgABAQAAAQABAA...
    
    ... to reference:
    
            ![](md_img_1611750760029220.jpg)
    
    # TODO: don't output as files, just return the data, caller of the function can decide what to do with data.
    """
    

    
    rx = r'!\[\]\(data:image/.*?,(.*?)\)'
    D = []
    lines = open(filename).readlines()
    imgNo = 1
    for l in lines:
        match = re.search(rx, l)
        if match is not None:
            imgData = match.group(1)
            imgData = base64.b64decode(imgData)
            
            # @@TODO: detect image type (jpg, png) from binary data
            filename_img = 'img_%0.4i.%s'  % (imgNo, guessImageExt(imgData))
            imgNo += 1
            fout = open(folderName + '/' + filename_img, 'wb')
            fout.write(imgData)
            
            l = '![](%s)' % filename_img
            
        D.append(l)
    
    return "".join(D)
        
        
if __name__ == '__main__':
    
    filename = 'challenge.md'
    
    # Eventually markdown just override + move out file handling out of raw md -> md'.
    folderName = os.path.splitext(filename)[0]
    assert not os.path.isdir(folderName)
    os.mkdir(folderName)
    
    data = markdownFix(filename, folderName)
    
    filename = folderName + '/' + filename
    open(filename, 'w').write(data)
    
