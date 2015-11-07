"""
Define where data is.
"""

import sys
import os

import platform

def dcoreDataRoot():
    """
    @@@global rename this as dcoreDataRoot
    """

    if platform.system().lower() == "windows":
        return r'c:\david\dcore_home'
    else:
        return os.path.expanduser('~/sync/dcore_data')

def pathExt():
	return os.path.normpath(os.path.join(dcoreDataRoot(), './path_ext'))
    
if __name__ == '__main__':
	print(dcoreDataRoot())
	print(pathExt())
