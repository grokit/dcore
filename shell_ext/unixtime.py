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
    
    parser.add_argument(
                        '-m', 
                        '--milliseconds_mode', 
                        action="store_true",
                        help='Use milliseconds instead of seconds since epoch.')

    parser.add_argument('time', 
                        type=int,
                        nargs='?',
                        help='Unix time to transform to readable date-time.')
    
    args = parser.parse_args()
    
    return args
    
def unixTimeToReadeableStr(unix_time):
    if unix_time > 2**35: # limitation of time.ctime
        raise ValueError("unix_time: %s is too large" % unix_time)
    
    dtc = datetime.datetime(*(time.gmtime(unix_time))[:6]).isoformat()
    return "localtime: %s\nutc time: %s" % (time.ctime(unix_time), dtc)

if __name__ == '__main__':
    
    args = getCommandLineArguments()
    print(args)
    
    if args.time is None:
        print(time.time())
        exit(0)
    
    unixTime = int(args.time)
    if args.milliseconds_mode:
        unixTime = unixTime / 1000
    
    print( unixTimeToReadeableStr( unixTime ) )
