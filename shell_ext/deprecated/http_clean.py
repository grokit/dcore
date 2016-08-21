"""
# TODO
- Have cmdline option to handle file.
"""

import re

_meta_shell_command = 'http_clean'

annoying = ['^Set-.*', '^Cookie:.*', 'Reg[^ ]*?:.*', '^S2SToken:.*']

if __name__ == '__main__':
    inputBuf = []
    while len(inputBuf) == 0 or inputBuf[-1].find('STOP!') == -1:
        try:
            lIn = input()
        except (EOFError):
            break        
        if lIn == None:
            break # reached EOF
        inputBuf.append( lIn )
    
    bufOut = []
    for line in inputBuf:
        for pattern in annoying:
            line = re.sub(pattern, pattern + ': [CENSORED]', line)
        bufOut.append(line)
    
    open('http_clean.txt', 'w').write("\n".join(bufOut))
