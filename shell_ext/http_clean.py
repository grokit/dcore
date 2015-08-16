
import re
#import sys

_meta_shell_command = 'http_clean'

annoying = ['^Set-.*', '^Cookie:.*', 'Reg[^ ]*?:.*']

if __name__ == '__main__':
    inputBuf = []
    while len(inputBuf) == 0 or inputBuf[-1].find('STOP!') == -1:
        lIn = input()
        if lIn == None:
            break # reached EOF
        inputBuf.append( lIn )
    
    bufOut = []
    for line in inputBuf:
        for pattern in annoying:
            line = re.sub(pattern, 'Removed: ' + pattern, line)
        bufOut.append(line)
    
    open('http_clean.txt', 'w').write("\n".join(bufOut))
