"""
History Grep
"""

import sys
import os
import re
import argparse

_meta_shell_command = 'hgr'


def getArgs():
    parser = argparse.ArgumentParser()
    # https://docs.python.org/3/library/argparse.html#nargs
    parser.add_argument('regex', nargs='+')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = getArgs()
    regex = " ".join(args.regex).strip()

    with open(os.path.expanduser('~/.bash_history'), 'r') as fh:
        for line in fh.readlines():
            line = line.strip()
            mm = re.search(regex, line)
            if mm is not None:
                print(line)
                #print(mm.group(0))
