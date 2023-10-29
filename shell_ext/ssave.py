"""
Save stdout/stderr piped in to a file.

# TODO
"""

import sys
import os
import datetime
import argparse

import dcore.data as data
import dcore.utils as utils

_meta_shell_command = 'ssave'

def get_args():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args

def find(folder, pattern, i):
    return os.path.expanduser(os.path.join(folder, f'{pattern}_{utils.date_now_iso_8601_safe_folder()}.log'))

if __name__ == '__main__':
    folder = os.path.join(data.logsdir(), 'ssave')
    G_ARGS = get_args()
    data.createDirIfNotExist(folder)

    pattern = 'ssave_capture'
    i = 0
    filename = find(folder, pattern, i)
    while os.path.exists(filename):
        i += 1
        filename = find(folder, pattern, i)

    data = sys.stdin.read()
    with open(filename, 'w') as fh:
        fh.write(data)

    print(f'data written in {filename}')

