"""
wget an entire website, then download all links matching a pattern.

Note: personalize mp3UrlToFilename(...) for the current website.
"""

_meta_shell_command = 'juice_website'

import os
import re

command = 'wget --mirror -p --convert-links -P ./ __url__'
command = command.replace('__url__', 'http://thehistoryofpodcast.blogspot.ca')
os.system(command)

def mp3UrlToFilename(url):
    try:
        url = url.lower()
        #url = "".join(url.split('/')[4:])
        bigName = url.split('/download/')[1].split('.')[0]
        epName = url.split('episode')[1].split('-')
        title = epName[1]
        epName = epName[0]
        fname = "%s_%.3i_%s" % (bigName, int(epName), title)
    except Exception as e:
        print('Fail on url %s' % url)
        fname = url
        #raise e
    allowed = 'abcdefghijklmnopqrstuvwxyz0123456789' 

    O = []
    for l in fname:
        if l in allowed:
            O.append(l)
        else:
            O.append('_')
    return "".join(O) + '.mp3'

def walkFiles():
    for (dirpath, dirnames, filenames) in os.walk('.'):
        for name in filenames:
            fileN = os.path.join(dirpath, name)
            yield fileN

def allUrls():
    for file in walkFiles():
        try:
            print('In file, ' +  file)
            content = open(file).read()

            m = re.findall(r'href[ "=]+(http://[^"\']+)', content)
            if len(m) > 0:
                for i in m:
                    if 'href' not in i:
                        yield i
        except Exception as e:
            print('Fail file: ' + file + '/' + str(e))

def filterAndTransformUrls(U):
    H = set()
    UOut = []
    for url in U:
        if url[-4:] == '.mp3':
            if url not in H:
                H.add(url)
                fname = mp3UrlToFilename(url)
                UOut.append((url, fname))
    return UOut

lst = [x for x in allUrls()]
lst = filterAndTransformUrls(lst)
#print(lst)

c = []
for it in lst:
    cmd = 'wget %s -O %s' % it
    print(cmd)
    os.system(cmd)

