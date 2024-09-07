"""
gg: open a file or directory with an appropriate application select on best guess.
"""

_meta_shell_command = 'gg'

import os
import sys
import argparse

import dcore.utils as utils

if __name__ == '__main__':
    args = " ".join(sys.argv[1:])
    utils.open_file_autoselect_app(args)
