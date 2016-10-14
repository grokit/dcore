#!/usr/bin/python3

"""
Rename file or folder with today's timestamp:

    myfile.txt -> 2016-08-20_myfile.txt

# BUGS

arch@arch-nx64:~/sync/archive/media_pics_and_videos/mine/2016$ rename_time_tag _/tata/
_/tata/ -> _/tata/2016-09-25_
Traceback (most recent call last):
File "/home/arch/sync/scripts/dcore/shell_ext/rename_time_tag.py", line 33, in <module>
  os.rename(f, to)
  OSError: [Errno 22] Invalid argument: '_/tata/' -> '_/tata/2016-09-25_'

"""

import re
import os
import argparse
import time
import datetime

_meta_shell_command = 'rename_time_tag'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    args = parser.parse_args()
    return args
    
def pre():
    return datetime.datetime.now().strftime("%Y-%m-%d")

if __name__ == '__main__':
    args = getArgs()
    f = args.filepath
    folder, file = os.path.split(args.filepath)

    to = os.path.join(folder, "%s_%s" % (pre(), file))
    print('%s -> %s' % (f, to))
    os.rename(f, to)
