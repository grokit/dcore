
import os

def getAllFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append( os.path.join(dirpath, f) )
    return F

<<<<<<< HEAD
F = getAllFiles('.')
F = [f for f in F if f[-3:] == '.py']
=======
def legitEnd(end):
    return end in ['.py', '.md', '.markdown', '.html', '.js']

F = getAllFiles('.')
F = [f for f in F if legitEnd(os.path.splitext(f)[1])]
>>>>>>> b5c776192e415919cd1af02f5d51a62420dd5184
for f in F:
    print(f)
    content = open(f).read()
    content = content.replace('\r\n', '\n')
<<<<<<< HEAD
=======
    #content = content.replace('\r', '')
>>>>>>> b5c776192e415919cd1af02f5d51a62420dd5184
    open(f,'w').write(content)
