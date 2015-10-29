
import os

def getAllFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append( os.path.join(dirpath, f) )
    return F

F = getAllFiles('.')
F = [f for f in F if f[-3:] == '.py']
for f in F:
    print(f)
    content = open(f).read()
    content = content.replace('\r\n', '\n')
    open(f,'w').write(content)
