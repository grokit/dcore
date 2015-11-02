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

def osExec(cmd):
    print(cmd)
    os.system(cmd)

def youtubedl_upgrade():
    osExec('sudo pip install --upgrade youtube_dl')

def mempigs():
    osExec('ps -e -o pid,vsz,comm= | sort -n -k 2')

def lock():
    osExec('gnome-screensaver-command -l')

def battery():
    osExec('upower -i /org/freedesktop/UPower/devices/battery_BAT0| grep -E "state|to\ full|percentage"')

def crashplan():
    command = '/usr/local/crashplan/bin/CrashPlanDesktop'
    print(command)
    osExec(command)

def wifi():
    #  wicd-curses does not seem to work...
    command = 'nm-applet&'
    print(command)
    osExec(command)

def tg():
    #  wicd-curses does not seem to work...
    cur = os.getcwd()
    path = os.path.expanduser('~/sync/apps/tg/')
    os.chdir(path)
    command = './bin/telegram-cli'
    print(command)
    osExec(command)
    os.chdir(cur)

def sleep():
    command = 'dbus-send --system --print-reply --dest="org.freedesktop.UPower" /org/freedesktop/UPower org.freedesktop.UPower.Suspend'
    osExec(command)

def apps():
    startapps()

def startapps():
    osExec('nohup dropbox start&')
    osExec('nohup diodon&')
    #osExec('nohup shutter --min_at_startup&')

def vol_up():
    osExec('amixer -q sset Master 10%+')

def vol_down():
    osExec('amixer -q sset Master 10%-')

def vol_mute_toggle():
    osExec('amixer -q sset Master toggle')
    osExec('amixer -q sset Headphone toggle')
    osExec('amixer -q sset Speaker toggle')
    osExec('amixer -q sset PCM toggle')

def unmute():
    osExec('amixer set Master unmute') 
    osExec('amixer set Headphone unmute') 
    osExec('amixer set Speaker unmute') 
    osExec('amixer set PCM unmute') 

def mute():
    osExec('amixer set Master mute')
    osExec('amixer set Headphone mute') 
    osExec('amixer set Speaker mute') 
    osExec('amixer set PCM mute') 

if __name__ == '__main__':
    args = getArgs()
    fnHash = {fnName: fn for fnName, fn in inspect.getmembers(sys.modules[__name__]) if inspect.isfunction(fn) and fnName != 'getArgs'}

    if args.command in fnHash:
        fn = fnHash[args.command]
        fn()
    else:
        print('Function %s not in function map:' % args.command)
        print("\t" + "\n\t".join( [fnName for fnName, fn in fnHash.items()] ))
