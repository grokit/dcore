"""
"""
import os
import dcore.apps.dnotes.search as search

_meta_shell_command = 'now'

if __name__ == '__main__':
    # ehm, would be better to just call python
    cmd = 'ns tag:::now'
    os.system(cmd)
