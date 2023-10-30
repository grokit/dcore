"""
Also see: date -d @ <time>

# TODO

- Would be great if it were bi-directional.        
"""

_meta_shell_command = 'unixtime'

# http://en.wikipedia.org/wiki/Unix_time

import time
import datetime
import sys
import argparse


def getCommandLineArguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('time',
                        type=float,
                        nargs='?',
                        help='Unix time to transform to readable date-time.')

    args = parser.parse_args()

    return args


def unixTimeToReadeableStr(unix_time):
    while unix_time > 2**35:  # limitation of time.ctime
        #raise ValueError("unix_time: %s is too large" % unix_time)
        unix_time = unix_time/1000

    dtc_local = (datetime.datetime.utcfromtimestamp(unix_time) +datetime.timedelta(seconds=datetime.datetime.now().astimezone().utcoffset().total_seconds())).astimezone()
    dtc = datetime.datetime.utcfromtimestamp(unix_time)
    return "localtime: %s\nutc time : %s" % (dtc_local, dtc)


if __name__ == '__main__':

    args = getCommandLineArguments()
    print(args)

    if args.time is None:
        print(f'unixtime ms: {int(1000*time.time())}')
        exit(0)

    unixTime = float(args.time)
    print(unixTimeToReadeableStr(unixTime))
