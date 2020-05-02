"""
"""
import os
import dcore.apps.dnotes.search as search

_meta_shell_command = 'now'

if __name__ == '__main__':
    # ehm, would be better to just call python
    # -m: show all, not just topx
    cmd = 'ns --number_of_matches_display 1000 tag:::now'
    os.system(cmd)
