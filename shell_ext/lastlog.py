"""
"""

_meta_shell_command = 'll'

import os
import argparse

def getArgs():
    parser = argparse.ArgumentParser()
    return parser.parse_args()
    
if __name__ == '__main__':
    args = getArgs()
    print(args)
    files = [f for f in os.listdir('.') if "log" in f.lower()]
    file = max(files, key=os.path.getctime)
    print(file)
    cmd = 'np %s' % file
    os.system(cmd)