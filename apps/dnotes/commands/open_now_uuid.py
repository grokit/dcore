"""
"""
import os
import dcore.apps.dnotes.search as search

_meta_shell_command = 'now'

import sys

if __name__ == '__main__':
    # ehm, would be better to just call python
    # -m: show all, not just topx
    cmd = 'ns --number_of_matches_display 1000 -t now %s' % " ".join(sys.argv[1:])
    print(cmd)
    os.system(cmd)
