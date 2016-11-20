"""
Shortcuts to Linux commands.

nux <command-name>

`command-name` are reflected so to add a command just declare a new function.

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

def youtubedl_upgrade():
	osExec('sudo pip install --upgrade youtube_dl')

def pdf():
	osExec('wine ~/.wine/drive_c/pdf/PDF\ Viewer/PDFXCview.exe&')

def sys_update():
	# http://askubuntu.com/questions/196768/how-to-install-updates-via-command-line
	osExec('sudo apt-get update')	   # Fetches the list of available updates
	osExec('sudo apt-get upgrade')	  # Strictly upgrades the current packages
	osExec('sudo apt-get dist-upgrade') # Installs updates (new ones)

def mempigs():
	osExec('ps -e -o pid,vsz,comm= | sort -n -k 2')

def mac():
    osExec('sudo ifconfig wlp1s0 down')
    osExec('sudo macchanger -r wlp1s0')
    osExec('sudo ifconfig wlp1s0 up')

def lock():
	osExec('gnome-screensaver-command -l')

def battery():
	osExec('upower -i /org/freedesktop/UPower/devices/battery_BAT0| grep -E "state|to\ full|percentage"')

def crashplan():
	command = '/usr/local/crashplan/bin/CrashPlanDesktop'
	print(command)
	osExec(command)

def low():
	osExec('xbacklight -set 15')

def med():
	osExec('xbacklight -set 50')

def high():
	osExec('xbacklight -set 100')

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
	osExec('nohup dropbox start > /dev/null&')
	osExec('nohup diodon > /dev/null&')
	#sshots()

def sshots():
	osExec('nohup shutter --min_at_startup > /dev/null&')

def vol_ctrl():
	osExec('pavucontrol')

def trackpad_on():
    osExec('xinput list')
    osExec('xinput set-prop 13 "Device Enabled" 1')

def trackpad_off():
    osExec('xinput list')
    osExec('xinput set-prop 13 "Device Enabled" 0')

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
