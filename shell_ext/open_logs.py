"""
"""

import os
import argparse

import dcore.data as data

_meta_shell_command = 'logs'


def getArgs():
    parser = argparse.ArgumentParser()
    return parser.parse_args()


if __name__ == '__main__':

    args = getArgs()
    folder = data.logsdir()
    print('Using folder: %s.' % folder)

    files = os.listdir(folder)
    files = [os.path.join(folder, f) for f in files]
    files = [f for f in files if os.path.isfile(f)]
    files.sort(key=lambda x: os.path.getmtime(x))

    if len(files) == 0:
        print('No log file found.')
    else:
        file = os.path.abspath(files[-1])
        cmd = 'vi %s' % file
        print(cmd)
        os.system(cmd)
