"""
New consecutive number.
"""

import os
import glob
import argparse
import shutil

import dcore.data as data
import dcore.utils as utils

_meta_shell_command = 'ncn'

def get_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()

    folder = os.path.join(data.dcoreData(), 'consecutive_number')
    data.createDirIfNotExist(folder)
    filename = os.path.join(folder, 'next.n')

    if os.path.isfile(filename):
        with open(filename, 'r') as fh:
            nn = fh.read().strip()
            nn = int(nn)
    else:
        nn = 1

    with open(filename, 'w') as fh:
        fh.write(str(nn+1))
    print(nn)


