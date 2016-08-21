"""
# Bugs

- Does not redirect stderr to notepad.
"""

import sys
import os
import tempfile

_meta_shell_command = 'tonp'

def getStdIn():
    
    all = []
    for line in sys.stdin:
        all.append(line)
    
    return " ".join(all)
    #return sys.stdin.read()

if __name__ == '__main__':
    
    data = getStdIn()
    
    fh = tempfile.NamedTemporaryFile(delete=False)
    fh.write(data.encode())
    fh.close()
    
    if os.name == 'posix':
        editor = os.environ.get('EDITOR','vim')
        print([editor, fh.name])
        subprocess.call([editor, fh.name])
    else:
        cmd = 'start /b np "%s"' % fh.name
        print(cmd)
        os.system(cmd)
    