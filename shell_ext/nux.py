"""
Shortcuts to Linux commands.

startx: 'sudo /etc/init.d/lightdm start'
"""

_meta_shell_command = 'nux'

import sys
import inspect
import argparse
import os

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', default = 'none', nargs='?')
    args = parser.parse_args()
    return args

def lock():
    os.system('gnome-screensaver-command -l')

def sleep():
    command = 'dbus-send --system --print-reply --dest="org.freedesktop.UPower" /org/freedesktop/UPower org.freedesktop.UPower.Suspend'
    os.system(command)

def startapps():
    os.system('nohup dropbox start&')
    os.system('nohup diodon&')
    os.system('nohup shutter --min_at_startup&')

def mute():
    os.system('amixer set Master mute')

def unmute():
    os.system('amixer set Master unmute')

if __name__ == '__main__':
    args = getArgs()
    fnHash = {fnName: fn for fnName, fn in inspect.getmembers(sys.modules[__name__]) if inspect.isfunction(fn) and fnName != 'getArgs'}

    if args.command in fnHash:
        fn = fnHash[args.command]
        fn()
    else:
        print('Function %s not in function map:' % args.command)
        print("\t" + "\n\t".join( [fnName for fnName, fn in fnHash.items()] ))
