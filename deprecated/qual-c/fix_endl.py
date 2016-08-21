
import os

def getAllFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append( os.path.join(dirpath, f) )
    return F

def legitEnd(end):
    return end in ['.py', '.md', '.markdown', '.html', '.js']

F = getAllFiles('.')
F = [f for f in F if legitEnd(os.path.splitext(f)[1])]

for f in F:
    print(f)
    content = open(f).read()
    content = content.replace('\r\n', '\n')
    open(f,'w').write(content)
