"""
"""

_meta_shell_command = 'll'

import os
import argparse

def getArgs():
    parser = argparse.ArgumentParser()
    return parser.parse_args()
<<<<<<< HEAD

=======
    
>>>>>>> b5c776192e415919cd1af02f5d51a62420dd5184
if __name__ == '__main__':
    args = getArgs()
    print(args)
    files = [f for f in os.listdir('.') if "log" in f.lower()]
    file = max(files, key=os.path.getctime)
    print(file)
    cmd = 'np %s' % file
    os.system(cmd)