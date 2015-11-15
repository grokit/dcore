"""
Do somethings with the last screenshot.
Defaul: copy to current directory.
"""

_meta_shell_command = 'sshere'

import os
import argparse
import shutil

def getArgs():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

if __name__ == '__main__':
    args = getArgs()
    print(args)

    sshotFolder = '/home/arch2/sync/dev/Dropbox/screenshots/scrot'

    files = [os.path.join(sshotFolder, f) for f in os.listdir(sshotFolder) if os.path.splitext(f)[1] == '.png']
    file = max(files, key=os.path.getctime)

    src = file
    dst = './' + os.path.split(file)[1]

    print('Copy `%s` to `%s`.' % (src, dst))
    shutil.copyfile(src, dst)
