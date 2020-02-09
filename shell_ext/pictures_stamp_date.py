"""
Stamp pictures date using imagemagick based on picture's exif metadata.
"""

_meta_shell_command = 'media_pictures_stamp_date'

import os
import subprocess


def isExt(exts, f):
    if '_stamped' in f: return False
    if len(f) < 4: return False
    for ext in exts:
        if f[-4:] == '.' + ext: return True
    return False


def getTime(f):
    match = "exif:DateTime:"
    cmd = 'identify -verbose %s' % f
    stdoutdata = subprocess.getoutput(cmd)

    for l in stdoutdata.splitlines():
        if match in l:
            m = l.split(match)[1].strip().split(' ')[0].strip().replace(
                ':', '_')
            return m

    raise Exception("Cannot get picture time: %s." % f)


def getFontSize(f):
    match = "exif:ExifImageLength:"
    cmd = 'identify -verbose %s' % f
    stdoutdata = subprocess.getoutput(cmd)

    for l in stdoutdata.splitlines():
        if match in l:
            m = l.split(match)[1].strip()
            return int(m) / 50

    raise Exception("Cannot get picture size: %s." % f)


if __name__ == '__main__':
    # http://www.imagemagick.org/Usage/annotating/
    cmd = "convert %s -fill '#0008' -gravity SouthWest  -fill white -background '#00000080'  -font  'FreeSans' -pointsize %s -annotate 0 '%s' %s"

    exts = ['jpg', 'png']
    F = os.listdir('.')
    F = [f for f in F if isExt(exts, f)]

    for f in F:
        t = getTime(f)
        fontSize = getFontSize(f)
        c = cmd % (f, fontSize, t.replace('_', '/'), f.replace(
            '.', '_stamped.'))
        print(c)
        os.system(c)
