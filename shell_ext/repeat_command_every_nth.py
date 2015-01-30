
import time
import os
import argparse

"""
_meta_shell_command = 'repeat'
"""

def getStdinData():
    return sys.stdin.read()

def repeat(command, timeInterval):
    
    while(1):
        os.system('cls')
        print("'%s' repeated every %s second(s):\n" % (command, timeInterval))
        os.system(command)
        time.sleep(timeInterval)
        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('command', nargs='+')
    parser.add_argument('-t', '--timeInterval', default = '1.0', type=float)
    
    args = parser.parse_args()
    
    timeInterval = 2
    
    if args.timeInterval is not None:
        timeInterval = args.timeInterval
    
    command = " ".join(args.command)
    
    repeat(command, timeInterval)

    
