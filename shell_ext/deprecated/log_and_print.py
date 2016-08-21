
import sys
import os
import time
import random

import misc.files

_meta_shell_command = 'lp'

def getStdinData():
    return sys.stdin.read()

# @@move to file:ext or something    


if __name__ == '__main__':
    
    data = getStdinData()
    
    fh = open( misc.files.getUniqueDateFile('log_and_print_'), 'wb' )
    fh.write(data.encode())
    fh.close()
    
    print(data)
    
    
    