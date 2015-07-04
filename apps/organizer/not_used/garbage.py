
def parseDocxMainDocumentXMLAsMarkdown_cowboyVersion(doc):    
    
    D = []
    p1m = '<w:t>'
    p2m = '</w:t>'
    
    enld = '<w:p'
    while True:
        
        p1 = doc.find(p1m)
        lbdetect = doc.find(enld)
        
        if lbdetect != -1 and lbdetect < p1:
            D.append('\n')
            doc = doc[lbdetect + len(enld):]
            continue
        
        if p1 == -1:
            break
        
        p2 = doc.find(p2m)
        
        txt = doc[p1+len(p1m):p2]
        D.append(txt)
        doc = doc[p2+len(p2m):]
        
    return "".join(D)
