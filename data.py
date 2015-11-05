"""
Define where data is.
"""

import sys
import os

def dcoreRoot():
    paths = []
    paths.append(os.path.expanduser('~/sync/dcore'))
    paths.append(r'c:\david\dcore_home')
    root = [f for f in paths if os.path.isdir(f)]
    assert len(root) == 1
    return root[0]

def pathExt():
    return r'c:\david\scripts-private\path_ext'
    
if __name__ == '__main__':
    pass