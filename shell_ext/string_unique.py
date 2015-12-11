"""
# TODO
"""

import re

_meta_shell_command = 'string_unique'

if __name__ == '__main__':
    inputBuf = []
    while len(inputBuf) == 0 or inputBuf[-1].find('!!!STOP!!!') == -1:
        try:
            lIn = input()
        except (EOFError):
            break        
        if lIn == None:
            break # reached EOF
        inputBuf.append( lIn )
    
    lines = set()
    for line in inputBuf:
        lines.add(line.strip())
    
    for line in lines:
        print(line)
    
