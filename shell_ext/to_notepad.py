
"""
# Bugs
- does not redirect stderr to notepad
- windows only
"""

import sys
import os
import tempfile
import time

import misc.osext as osext

_meta_shell_command = 'tonp'

def getAndPrintStdinData():
    
    all = []
    for line in sys.stdin:
        all.append(line)
        print(line, end='')
    
    return " ".join(all)
    #return sys.stdin.read()

if __name__ == '__main__':
    
    data = getAndPrintStdinData()
    
    fh = tempfile.NamedTemporaryFile(delete=False)
    fh.write(data.encode())
    fh.close()
    
    cmd = 'start /b np "%s"' % fh.name
    print(cmd)
    #osext.execute(cmd) # does not work, maybe because it uses a temp file too and delete the other one?
    os.system(cmd)
    
    
