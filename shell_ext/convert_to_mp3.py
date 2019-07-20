
import sys
import os
import argparse
import glob 

_meta_shell_command = 'convert_to_mp3'

def getArgs():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

if __name__ == '__main__':
    args = getArgs()
    files = list(glob.iglob('.' + '/**/*.**', recursive=True))

    files = [f for f in files if f[-4:] == '.mp4']
    for fi in files:
        print(fi)
        frm = fi
        to = fi.replace('/', '_').replace('.', '_')[0:-4] + '.mp3'
        cmd = 'ffmpeg -i %s %s' % (frm, to)
        print(cmd)
        os.system(cmd)

