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
    cmd = "identify -verbose '%s'" % f
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

    return M

def shouldResize(meta):
    # Old way: just look at file size:
    # return (os.path.getsize(file) / (1024**2)) > 0.800

    if meta["Width"] > 2048 or meta["Height"] > 2048:
        return True

    if meta["Quality:"] > 80:
        return True

    return False

def getAllFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append(os.path.normpath(os.path.join(dirpath, f)))
    #F = [os.path.abspath(f) for f in F]
    return F

if __name__ == '__main__':

    args = getArgs()
    
    #files_all = os.listdir('.')
    files_all = getAllFiles()
    reg = re.compile(fnmatch.translate('*.jpg'), re.IGNORECASE)
    files = [file for file in files_all if reg.match(file) is not None]
    
    for file in files:
        try:
            meta = getPictureMetadata(file)
            if shouldResize(meta):
                cmd = "mogrify -resize \"2048x2048>\" -quality 80 '%s'" % file
                if args.apply:
                    print(meta)
                    print(cmd)
                    os.system(cmd)
                else:
                    print('Not applied: ', meta)
            else:
                print("Skipping: %s." % (meta))
        except Exception as e:
            print('Exception: %s. Not processing %s.' % (e, file))
    
