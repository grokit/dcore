"""
Save stdout/stderr piped in to a file.

# TODO
"""

import sys
import os
import datetime
import argparse
import string

import dcore.data as data
import dcore.utils as utils

_meta_shell_command = 'ssave'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', '-t', default='')
    args = parser.parse_args()
    return args

def find_next_file(folder, pattern, title, i):
    suffix = ''
    datestr = utils.date_now_iso_8601_safe_folder() 
    if i > 0:
        suffix = f'.coll_{i:04d}'
    if len(title) > 0:
        title = f'_{title}'
    return os.path.expanduser(os.path.join(folder, f'{pattern}_{datestr}{title}{suffix}.log'))

if __name__ == '__main__':
    folder = os.path.join(data.logsdir(), 'ssave')
    G_ARGS = get_args()
    data.createDirIfNotExist(folder)

    title = G_ARGS.title
    pattern = 'ssave_capture'
    i = 0
    filename = find_next_file(folder, pattern, title, i)
    while os.path.exists(filename):
        i += 1
        filename = find_next_file(folder, pattern, title, i)

    data = sys.stdin.read()
    with open(filename, 'w') as fh:
        fh.write(data)

    print(f'data written in {filename}')

