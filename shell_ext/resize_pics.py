
import sys
import os
import tempfile
import time
import glob
import re
import fnmatch

_meta_shell_command = 'resize_pics'

def getStdinData():
    return sys.stdin.read()

if __name__ == '__main__':
    
    reg = re.compile(fnmatch.translate('*.jpg'), re.IGNORECASE)
    
    files_all = os.listdir('.')
    
    files = [file for file in files_all if reg.match(file) is not None]
    
    for file in files:
        
        if (os.path.getsize(file) / (1024**2)) > 0.800:
            cmd = 'mogrify -resize "2048x2048>" -quality 80 %s' % file
            #cmd = 'mogrify -resize "800x800>" -quality 80 %s' % file
            print(cmd)
            os.system(cmd)
        else:
            print("Skipping small file: %s." %file)
    
    
    
