"""

Finds video files, convert to mp3 in a flattened structure.

# Misc

Convert all files to single: 
    - Don't use mp3wrap, will not play correctly. 
    - ffmpeg -i "concat:file1.mp3|file2.mp3" -acodec copy out.mp3
"""

import sys
import os
import argparse
import glob 

_meta_shell_command = 'convert_to_mp3'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--apply', action='store_true', default=False, help='Inverse of all talk no do.')
    return parser.parse_args()

def select():
    return [f for f in files if f[-4:] == '.mp4']

def convert_to(files, args):
    for fi in files:
        print(fi)
        frm = fi
        to = fi.replace('/', '_').replace('.', '_')[0:-4] + '.mp3'
        cmd = 'ffmpeg -i %s %s' % (frm, to)
        print(cmd)
        if args.apply:
            os.system(cmd)

def join(files):
    """
    joined_name -> files
    """

    nums = set('0123456789')

    joined_files = {}
    for ff in files:
        n = None
        for c in ff:
            if c not in nums and n is not None:
                break
            if c in nums:
                if n is None:
                    n = int(c)
                else:
                    n = n*10 + int(c)
        assert n is not None
        n = str(n)
        if n not in joined_files: joined_files[n] = set()
        joined_files[n].add(ff)
    return joined_files


def apply_join(joined_files, args):
    # E.g. 'ffmpeg -i "concat:file1.mp3|file2.mp3" -acodec copy out.mp3'
    for k, v in joined_files.items():
        cmd = 'ffmpeg -i "concat:%s" -acodec copy out_%s.mp3'
        cmd = cmd % ("|".join(v), k)
        #print(cmd)
        if args.apply:
            os.system(cmd)

if __name__ == '__main__':
    args = getArgs()
    files = list(glob.iglob('.' + '/**/*.**', recursive=True))
    files = [f for f in files if f[-4:] == '.mp4']
    joined_files = join(files)
    #print(joined_files)
    apply_join(joined_files, args)



