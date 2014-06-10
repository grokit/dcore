
_meta_shell_command = 'unixtime'

# http://en.wikipedia.org/wiki/Unix_time

import time
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
                        help='Unix time to transform to readable date-time.')
    
    args = parser.parse_args()
    
    return args
    
def unixTimeToReadeableStr(unix_time):
    if unix_time > 9e9:
        raise ValueError("unix_time: %s is > 2255, value is too large" % unix_time)
    
    # time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.ctime(unix_time))
    return time.ctime(unix_time)

if __name__ == '__main__':
    
    args = getCommandLineArguments()
    print(args)
    
    unixTime = int(args.time)
    if args.milliseconds_mode:
        unixTime = unixTime / 1000
    
    print( unixTimeToReadeableStr( unixTime ) )