"""
Define where data is.
"""

import sys
import os

def dcoreRoot():
    paths = []
    paths.append(os.path.expanduser('~/sync/dcore_data'))
    paths.append(r'c:\david\dcore_home')
    root = [f for f in paths if os.path.isdir(f)]
    if len(root) != 1:
        raise Exception('root != 1: %s' % root)
    return root[0]

def pathExt():
	return os.path.normpath(os.path.join(dcoreRoot(), './path_ext'))
    
if __name__ == '__main__':
	print(dcoreRoot())
	print(pathExt())
