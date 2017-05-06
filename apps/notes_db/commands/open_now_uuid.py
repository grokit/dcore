"""
"""
import os

_meta_shell_command = 'now'

if __name__ == '__main__':
    # ehm, would be better to just call python 
    cmd = 'ns -o tag:::now'
    os.system(cmd)
