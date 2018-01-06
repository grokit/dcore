"""
Detect large pictures, resize them to lower size / quality.

Dependencies: imagemagick
"""

import sys
import os
import re
import fnmatch
import argparse
import subprocess

_meta_shell_command = 'pictures_resize'

def getArgs():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--apply', action='store_true', default=False, help='Do the resize instead of just listing intentions.')
    args = parser.parse_args()
    return args

def getPictureMetadata(f):
    cmd = 'identify -verbose %s' % f
    stdoutdata = subprocess.getoutput(cmd)

    # Do not use: "exif:ExifImageLength:", "exif:ExifImageWidth:",
    # ... since it does not get updated after resize.
    metas = [ "Quality:", "Geometry:"]

    M = {}
    M['filename'] = f

    for l in stdoutdata.splitlines():
        for meta in metas: 
            if meta in l:
                assert meta not in M
                m = l.split(meta)[1].strip()
                M[meta] = m
                if meta == "Quality:":
                    M[meta] = int(M[meta])


    g = M["Geometry:"]
    M["Width"] = int(g.split('x')[0])
    M["Height"] = int(g.split('x')[1].split('+')[0])

    for m in metas:
        if m not in M:
            raise Exception("Cannot get meta: %s for image: %s." % (m, f))

    print(M)
    return M


def shouldResize(f):
    # Old way: just look at file size:
    # return (os.path.getsize(file) / (1024**2)) > 0.800

    M = getPictureMetadata(f)
    if M["Width"] > 2048 or M["Height"] > 2048:
        return True

    return False

if __name__ == '__main__':

    args = getArgs()
    
    reg = re.compile(fnmatch.translate('*.jpg'), re.IGNORECASE)
    files_all = os.listdir('.')
    files = [file for file in files_all if reg.match(file) is not None]
    
    for file in files:
        if shouldResize(file):
            cmd = 'mogrify -resize "2048x2048>" -quality 80 %s' % file
            if args.apply:
                print(cmd)
                os.system(cmd)
            else:
                print('Not applied: ', cmd)
        else:
            print("Skipping: %s." %file)
    
