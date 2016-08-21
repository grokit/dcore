
import argparse
import codecs
import os
import json

_meta_shell_command = 'files_index_cmp'

def argParse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--before', type=str)
    parser.add_argument('-a', '--after', type=str)
    
    args = parser.parse_args()
    return args

class FileMeta:
    
    def __init__(self):
        pass
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "%s, %s, %s" % (self.fullPath, self.hash, self.size)
    
def jsonListToFileHashes(ll):
    
    fHashes = []
    
    for l in ll:
        dJ = json.loads(l)
        
        fileMeta = FileMeta()
        
        fileMeta.fullPath = dJ['full_path'] # @@why fullPath in the past?
        fileMeta.hash = dJ['hash']
        fileMeta.size = int(dJ['size'])
        fHashes.append(fileMeta)
    return fHashes        

def checkDuplicates(lMeta):
    
    hashes = {}
    duplicates = []
    for meta in bef:
        
        if hashes.get(meta.hash) != None:
            l = meta
            r = hashes.get(meta.hash)
            if l.size != 0 and r.size != 0:
                duplicates.append((l, r))
        
        hashes[meta.hash] = meta
    
    if len(duplicates) != 0:
        print('Duplicates:')
        
        for dup in duplicates:
            print("%s and %s." % (dup[0], dup[1]))

def matchMetaToMetaSet(meta, metaSet):
    
    for m in metaSet:
        if meta.hash == m.hash and meta.size == m.size:
            return True
    
    return False

def changesFromAtoB(A, B):
    """
    We use only the filename and not fullpath because if we just renamed a folder we do not want to flag all the folder's files to be marked as changed.
    """
    
    fnpH = {}
    for meta in B:
        fileNoPath = os.path.split(meta.fullPath)[1]
        
        if fnpH.get(fileNoPath) is None:
            fnpH[fileNoPath] = [meta]
        else:
            fnpH[fileNoPath].append(meta)
    
    notFound = []
    for meta in A:
        fileNoPath = os.path.split(meta.fullPath)[1]
        
        found = False
        if fnpH.get(fileNoPath) is not None:
            if matchMetaToMetaSet(meta, fnpH[fileNoPath]):
                found = True
        
        if found == False:
            # Could check if hash there to suggest that it has been renamed.
            notFound.append(str(meta))
    
    return notFound    

"""    
def likelyModified(A, B):
    return notFound   
"""

if __name__ == '__main__':
    
    args = argParse()
    
    fh = codecs.open(args.before, 'r', encoding='utf8')
    before = fh.readlines()
    fh.close()
    
    fh = codecs.open(args.after, 'r', encoding='utf8')
    after = fh.readlines()
    fh.close()    
    
    bef = jsonListToFileHashes(before)
    aft = jsonListToFileHashes(after)
    
    aToB = changesFromAtoB(bef, aft)
    bToA = changesFromAtoB(aft, bef)
    #likelyModified = likelyModified(bef, aft)
    
    ## TODO: do this in 1 pass
    ## TODO: changed: filename is the same, but different hash
    
    fh = codecs.open('filesIndex_deleted', 'w', encoding='utf8')
    fh.write("\r\n".join(aToB) + "\r\n")
    fh.close()
    
    fh = codecs.open('filesIndex_new', 'w', encoding='utf8')
    fh.write("\r\n".join(bToA) + "\r\n")
    fh.close()
    
    
    
