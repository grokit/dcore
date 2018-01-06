"""
Detect large pictures, resize them to lower size / quality.

Dependencies: imagemagick
"""

import sys
import os
import re
import fnmatch
import argparse

_meta_shell_command = 'pictures_resize'

def getArgs():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--apply', action='store_true', default=False, help='Do the resize instead of just listing intentions.')
    
    """
    parser.add_argument('subject', default = ['NONE'], nargs='*')
    parser.add_argument('-t', '--to', default= private_data.primary_email)
    parser.add_argument('-f', '--attachment_filename')
    parser.add_argument('-w', '--work_email', action='store_true', default=False, help='Send to work e-mail instead of default one.')
    """
    
    args = parser.parse_args()
    return args

def getPictureMetadata(f):
    cmd = 'identify -verbose %s' % f
    stdoutdata = subprocess.getoutput(cmd)

    metas = ["exif:ExifImageLength:", "exif:ExifImageWidth:", "Quality:"]

    M = {}

    for l in stdoutdata.splitlines():
        for meta in metas: 
            if meta in l:
                m = l.split(meta)[1].strip()
                M[meta] = int(m) 

    for m in metas:
        if m not in M:
            raise Exception("Cannot get meta: %s for image: %s." % (m, f))

    return M


def shouldResize(f):
    # Old way: just look at file size:
    # return (os.path.getsize(file) / (1024**2)) > 0.800

    M = getPictureMetadata(f)
    if M["exif:ExifImageLength:"] > 2048 || M["exif:ExifImageWidth:"] > 2048:
        return True

    return False

if __name__ == '__main__':

    args = getArgs()
    
    reg = re.compile(fnmatch.translate('*.jpg'), re.IGNORECASE)
    files_all = os.listdir('.')
    files = [file for file in files_all if reg.match(file) is not None]
    
    for file in files:
        if shouldResize(f):
            cmd = 'mogrify -resize "2048x2048>" -quality 80 %s' % file
            if args.apply:
                print(cmd)
                os.system(cmd)
            else:
                print('Not applied: ', cmd)
        else:
            print("Skipping: %s." %file)
    
