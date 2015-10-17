
import read_docx
import read_img
import read_generic

import os

def getAllFiles(rootdir):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append( os.path.join(dirpath, f) )
    return F

def decideFolder(f):
    cat = None
    if os.path.splitext(f)[1] == 'docx':
        try:
            cat = read_docx.getCreatedAt(f)
        except Exception as e:
            print(e)
    
    if cat is None:
        cat = read_generic.getCreatedAt(f)
    
    if cat is not None:
        pass
    else:
        cat = 'unknown_time'
    
    return cat

if __name__ == '__main__':    
    F = getAllFiles('.')
    for f in F:
        folder = decideFolder(f)
        folder = os.path.join(os.getcwd(), 'out', folder)
        print(f, folder)
        
    open('_','wb').write("\n".join(F).encode())
        