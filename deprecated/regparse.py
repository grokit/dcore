"""
Experimental lib
"""

import re

def fileToEventList(filename, regex, filter = None):
    fh = open(filename, 'r')
    lines = fh.readlines()
    fh.close()

    events = []
    for line in lines:
        m = re.search(regex, line)
        if m is not None:
            
            if filter is None:
                events.append(m.group(1).strip())
            else:
                toAdd = False
                for f in filter:
                    if f in m.group(1):
                        toAdd = True
                
                if toAdd:
                    events.append(m.group(1).strip())

    return events

def chunk(events, nchunks):
    chunkLen = int(len(events) / nchunks)
    
    i = 0
    chunks = []
    while i < len(events) -1:
        chunks.append( events[i:i+chunkLen] )
        i += chunkLen    
    return chunks

def eventsToOccur(events):
    
    occurs = {}
    for e in events:
        if occurs.get(e) is None:
            occurs[e] = 1
        else:
            occurs[e] += 1
    
    #print(occurs)
    return occurs
    
def occurDictsToTable(occursDict):
    
    #print(occursDict)
    
    masterDict = {}
    for d in occursDict:
        for k, v in d.items():
            if masterDict.get(k) is None:
                masterDict[k] = v
            else:
                masterDict[k] += v
    
    #print(masterDict)
    
    headers = []
    for k, v in masterDict.items():
        headers.append(k)
    headers = [headers]
    
    for d in occursDict:
        newHorz = []
        
        for h in headers[0]:
            if d.get(h) == None:
                newHorz.append(0)
            else:
                newHorz.append(d[h])
        
        headers.append(newHorz)
        
   
    txtLines = []
    
    for h in headers:
        #print(h)
        
        h = list( map( lambda x : str(x), h ))
        
        txtLines.append(", ".join(h))
    
    return "\n".join(txtLines)
