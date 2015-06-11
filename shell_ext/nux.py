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

def battery():
    os.system('upower -i /org/freedesktop/UPower/devices/battery_BAT0| grep -E "state|to\ full|percentage"')

def crashplan():
    command = '/usr/local/crashplan/bin/CrashPlanDesktop'
    print(command)
    os.system(command)

def wifi():
    #  wicd-curses does not seem to work...
    command = 'nm-applet&'
    print(command)
    os.system(command)

def sleep():
    command = 'dbus-send --system --print-reply --dest="org.freedesktop.UPower" /org/freedesktop/UPower org.freedesktop.UPower.Suspend'
    os.system(command)

def apps():
    startapps()

def startapps():
    os.system('nohup dropbox start&')
    os.system('nohup diodon&')
    os.system('nohup shutter --min_at_startup&')

def vol_up():
    os.system('amixer -q sset Master 10%+')

def vol_down():
    os.system('amixer -q sset Master 10%-')

def vol_mute_toggle():
    os.system('amixer -q sset Master toggle')
    os.system('amixer -q sset Headphone toggle')
    os.system('amixer -q sset Speaker toggle')
    os.system('amixer -q sset PCM toggle')

def unmute():
    os.system('amixer set Master unmute') 
    os.system('amixer set Headphone unmute') 
    os.system('amixer set Speaker unmute') 
    os.system('amixer set PCM unmute') 

def mute():
    os.system('amixer set Master mute')
    os.system('amixer set Headphone mute') 
    os.system('amixer set Speaker mute') 
    os.system('amixer set PCM mute') 

if __name__ == '__main__':
    args = getArgs()
    fnHash = {fnName: fn for fnName, fn in inspect.getmembers(sys.modules[__name__]) if inspect.isfunction(fn) and fnName != 'getArgs'}

    if args.command in fnHash:
        fn = fnHash[args.command]
        fn()
    else:
        print('Function %s not in function map:' % args.command)
        print("\t" + "\n\t".join( [fnName for fnName, fn in fnHash.items()] ))
