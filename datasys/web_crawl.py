"""
Web-crawler to allow archiving part of the web.

# Use-Cases

- Save a complete demain and immediate resources.
- Save all mp3 under a domain with depth limit of 10.
- Save all first-degree references outside of the domain as .pdf.
"""

import urllib.request
import urllib.parse
import re

def fixUrl(u):
    return u.replace(' ', '%20')

class WebNode:
    """
    Essentially the web is a set of WebNodes linked together.

    Every WebNode has a URL which acts as a uniquely identifier. 
    
    However, there is no guarantee that a URL is unique (a webserver can have more than 1 URL map to the same document, creating possibility for infinite depth of repeated content).
    """

    def __init__(self, url):
        self.url = fixUrl(url)
        
        # URL -> WebNode
        self.links = {}

        # Content remains None until WebNode has been fetched from the web.
        self.content = None 

    def fetchSelf(self):
        content, links = downloadAndParse(self)
        self.content = content
        links = mergeLinksWithRootUrl(links, self.url)
        self.links = self.__fetchLinks(links)

    def __fetchLinks(self, linksList):
        links = {l: None for l in linksList}
        for k, v in links.items():
            links[k] = fetchContent(k) 
        return links

    def __str__(self):
        return '%s: %s' % (self.url, self.links)

def downloadAndParse(wnode):
    content = fetchContent(wnode.url)
    links = parseLinksFromWebBytes(content)
    L = []
    for l in links:
        L.append(fixUrl(l))
    return content, L

def downloadUrl(url):

    #sock =  urllib.request.urlopen(url)
    #mp3_bytes = sock.read()
    #sock.close()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    rbytes = urllib.request.urlopen(req).read()
    return rbytes

def fetchContent(url):
    print('fetchContent: ' + url)
    return downloadUrl(url)

def mergeLinksWithRootUrl(links, rootUrl):
    if rootUrl[-1] == '/': rootUrl = rootUrl[0:-1]
    L = []
    for l in links:
        if l.find('http') != 0:
            if l[0] == '/': l = l[1:]
            l = rootUrl + '/' +  l
        L.append(l)
    return L 

def parseLinksFromWebBytes(b):
    links = []

    html = b.decode("utf-8") 

    buff = html
    while len(buff) > 0:
        m = re.search(r'<[ ]*a.*?href.*?=[ ]*"(.*?)"', buff)
        if m is not None:
            c = m.group(1).strip()
            links.append(c)
            # m.end(x) returns the position m.group(x) ended.
            buff = buff[m.end(1)+1:]
        else:
            buff = ''

    return links

def fetchContentMock(url):
    return b'abc <a href="webpage"/a> tde'

#fetchContent= fetchContentMock 

if __name__ == '__main__':
    root = WebNode('http://www.grokit.ca/')
    root.fetchSelf()
    print(root)

