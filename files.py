import os
import shutil
import time

PATTERN = '.v%.2d'


def getUniqueDateFile(base, ext='.txt'):
    filename = time.strftime("%Y-%m-%d_") + base + ext

    # Postfix with file version, keep picking new names if prior versions already exit.
    n = 1
    while n == 1 or os.path.isfile(filename):
        pre, ext = os.path.splitext(filename)

        if os.path.splitext(pre)[1] != '' and os.path.splitext(
                pre)[1] == PATTERN % (n - 1):
            pre2, ext2 = os.path.splitext(pre)
            ext2 = ext2.replace(PATTERN % (n - 1), '')
            pre = pre2 + ext2

        ext = "%s%s" % (PATTERN % n, ext)
        n += 1
        filename = pre + ext

    return filename
