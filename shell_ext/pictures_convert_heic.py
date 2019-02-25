"""
Dependencies: imagemagick
"""

import sys
import os
import re
import fnmatch
import argparse
import subprocess

_meta_shell_command = 'pictures_convert_heic'

def getArgs():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = getArgs()
    
    files = [f for f in os.listdir('.') if f[-5:] == '.heic']
    for file in files:
        cmd = "heif-convert -q 80 %s %s" % (file, file[0:-5] + '.jpg')
        print(cmd)
        os.system(cmd)
