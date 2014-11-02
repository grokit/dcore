
import sys
import re

_meta_shell_command = 'windbg_cleantrace'

def getStdinData():
    return sys.stdin.read()

if __name__ == '__main__':
    
    data = getStdinData()
    
    lines_out = []
    for line in data.splitlines():
        
        line = re.sub(r'^[0-9A-Z` ]* : ', r'', line)
        lines_out.append(line)
    
    for line in lines_out:
        print(line)
    
    