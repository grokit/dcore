"""
"""

import os
import shutil
import argparse

_meta_shell_command = 'downloads_clear'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--apply', action="store_true", help='Clean the dir. Otherwise, just list.')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    loc = os.path.expanduser('~/Downloads')
    if not args.apply:
        print('ls %s' % loc)
        for ff in os.listdir(loc):
            print(ff)
    else:
        for ff in os.listdir(loc):
            ff = os.path.join(loc, ff)
            print('del %s' % ff)
            if os.path.isfile(ff):
                os.remove(ff)
            else:
                shutil.rmtree(ff)
