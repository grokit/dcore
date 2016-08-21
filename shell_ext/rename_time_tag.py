#!/usr/bin/python3

"""
Rename file with today's time-stamp:

    myfile.txt -> 2016-08-20_myfile.txt
"""

import re
import os
import argparse
import time
import datetime

_meta_shell_command = 'rename_time_tag'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    return args
    
def pre():
    return datetime.datetime.now().strftime("%Y-%m-%d")

if __name__ == '__main__':
    args = getArgs()
    f = args.filename

    to = "%s_%s" % (pre(), f)
    print('%s -> %s' % (f, to))
    os.rename(f, to)
