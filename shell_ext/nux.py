"""
Shortcuts to Linux commands.

I use this maily together with i3, where i3 shortcuts map to commands in this script.
e
# Usage

nux <command-name>

`command-name` are reflected so to add a command just declare a new function.

# Misc Notes

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
    if type(cmd) == type([]):
        for c in cmd:
            osExec(c)
    print(cmd)
    os.system(cmd)

def sleep():
    osExec('sudo pm-suspend')

def keybfr():
    # Get list of all keyboards available: localectl list-x11-keymap-layouts
    osExec('setxkbmap ca') # ca is the proper fr keyboard :).

def keyben():
    osExec('setxkbmap us')

def youtubedl_upgrade():
    osExec('sudo pip3 install --upgrade youtube_dl')

"""
def pdf():
    osExec('wine ~/.wine/drive_c/pdf/PDF\ Viewer/PDFXCview.exe&')
"""

def mempigs():
    osExec('ps -e -o pid,vsz,comm= | sort -n -k 2')

def screenshot():
    # -c: clipboard
    #osExec('sleep 5 && gnome-screenshot -a -c')
    #osExec('gnome-screenshot -a -c')

    # saves directly to file
    #osExec('scrot -s')
    osExec('scrot -s -e \'xclip -selection clipboard -t "image/png" < $f\' /tmp/scrot.png')

def ss():
    screenshot()

def mac():
    # Randomize MAC address. You may need to disconnect, reconnect.
    osExec('sudo ifconfig wlp1s0 down')
    osExec('sudo macchanger -r wlp1s0')
    osExec('sudo ifconfig wlp1s0 up')

def nupdate():
    # check number of update available
    osExec('/usr/lib/update-notifier/apt-check')

def update():
    osExec('sudo apt update --yes')

def lock():
    osExec('gnome-screensaver-command -l')
    #osExec('i3lock') # Big ugly white, and both screensavers sometimes overlap.

def urltopdf():
    # would need to fwd args
    osExec('wkhtmltopdf')

def battery():
    osExec('upower -i /org/freedesktop/UPower/devices/battery_BAT0| grep -E "state|to\ full|percentage"')

# - - - - - - - - - -  SCREEN

# screen-low
def slowww():
    #osExec('xbacklight -set 20') # At very low values my screen does a weird nose.
    osExec('xrandr --output eDP-1 --brightness 0.2')

def sloww():
    osExec('xrandr --output eDP-1 --brightness 0.4')

def slow():
    osExec('xrandr --output eDP-1 --brightness 0.5')

def smed():
    #osExec('xbacklight -set 50')
    osExec('xrandr --output eDP-1 --brightness 0.7')

def shigh():
    #osExec('xbacklight -set 100')
    osExec('xrandr --output eDP-1 --brightness 1.0')

def shighh():
    osExec('xrandr --output eDP-1 --brightness 1.5')

# - - - - - - - - - -  SCREEN END

def wifi():
    #  wicd-curses does not seem to work...
    command = 'nm-applet&'
    osExec(command)

def tg():
    #  wicd-curses does not seem to work...
    cur = os.getcwd()
    path = os.path.expanduser('~/sync/apps/tg/')
    os.chdir(path)
    command = './bin/telegram-cli'
    osExec(command)
    os.chdir(cur)

def sleep():
    command = 'dbus-send --system --print-reply --dest="org.freedesktop.UPower" /org/freedesktop/UPower org.freedesktop.UPower.Suspend'
    osExec(command)

def apps():
    startapps()

def startapps():
    "Used in i3 startup, do not rename."

    osExec('nohup dropbox start > /dev/null&')
    osExec('nohup shutter --min_at_startup > /dev/null&')

    # Security hazard...
    #osExec('nohup diodon > /dev/null&')

def size():
    osExec('du -hs * | sort -h')

def trackpad_on():
    osExec('xinput list')
    cmd ='xinput set-prop 13 "Device Enabled" 1' 
    print(cmd)
    print('Execute above command only if device match.')
    #osExec(cmd)

def trackpad_off():
    osExec('xinput list')
    cmd = 'xinput set-prop 13 "Device Enabled" 0'
    print(cmd)
    print('Execute above command only if device match.')
    #osExec(cmd)

def vol_ctrl():
    osExec('pavucontrol')

def vol_more_than_max():
    # See pavucontrol for a UI for those settings.
    osExec('pacmd set-sink-volume 0 85000')

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

def update():
    # This does not upgrade the distribution, it justs updates
    # all packages on system.
    # http://askubuntu.com/questions/196768/how-to-install-updates-via-command-line
    osExec('sudo apt-get update')        # Fetches the list of available updates
    osExec('sudo apt-get upgrade')       # Strictly upgrades the current packages
    osExec('sudo apt-get dist-upgrade')  # Installs updates (new ones)

if __name__ == '__main__':
    args = getArgs()
    fnHash = {fnName: fn for fnName, fn in inspect.getmembers(sys.modules[__name__]) if inspect.isfunction(fn) and fnName != 'getArgs'}

    if args.command in fnHash:
        fn = fnHash[args.command]
        fn()
    else:
        print('Function %s not in function map:' % args.command)
        fns = [fnName for fnName, fn in fnHash.items()] 
        fns.sort()
        print("\t" + "\n\t".join(fns))
