"""
Move files & folders to a new folder, except for <x>.
"""

import argparse
import os
import shutil

_meta_shell_command = 'magic_move'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_folder')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    output_folder = os.path.normpath(os.path.expanduser(args.output_folder))

    to_move = []
    os.makedirs(output_folder, exist_ok=True)

    data = os.listdir('.')
    data = [os.path.normpath(dd) for dd in data]
    # skip output folder, or folder beginning with a number
    data = [dd for dd in data if (dd is not output_folder) and (not (os.path.isdir(dd) and dd[0].isdigit()))]

    for dd in data:
        src, dst = dd, output_folder
        print(f'move {src} {dst}')
        shutil.move(src, dst)
