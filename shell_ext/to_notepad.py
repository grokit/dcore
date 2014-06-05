
"""
# Bugs
- does not redirect stderr to notepad
- windows only
"""

import sys
import os
import tempfile
import time

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
    os.system(cmd)
    
    
