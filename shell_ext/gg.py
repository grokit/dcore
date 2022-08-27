"""
gg: open a file or directory with the default os application.
"""

_meta_shell_command = 'gg'

import os
import sys
import argparse

if __name__ == '__main__':
    args = " ".join(sys.argv[1:])
    #older ubuntu:
    #cmd = "xdg-open '%s'" % args
    cmd = "gio open '%s'" % args
    print(cmd)
    os.system(cmd)
