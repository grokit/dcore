"""
Shortcuts to Windows commands.
"""

_meta_shell_command = 'win'

import sys
import inspect
import argparse
import os

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', default = 'none', nargs='?')
    args = parser.parse_args()
    return args

def get_process_path():
    os.system('PowerShell Get-Process ^| Format-List Path')

def apps():
    startapps()

def chmod_777():
    os.system('icacls "." /grant Everyone:(F) /T')

def startapps():
    os.system(r'start C:\david\app\launchy\Launchy.exe')
    os.system(r'start C:\david\app\ditto\Ditto.exe')
    os.system(r'start C:\david\app\autohotkey\AutoHotkey.exe C:\david\scripts-private\autohotkey\Work_AutoHotkey.ahk')
    os.system(r'start C:\david\app\greenshot\Greenshot.exe')
    # os.system(r'start C:\david\app\conemu\ConEmu64.exe')
    
if __name__ == '__main__':
    args = getArgs()
    fnHash = {fnName: fn for fnName, fn in inspect.getmembers(sys.modules[__name__]) if inspect.isfunction(fn) and fnName != 'getArgs'}

    if args.command in fnHash:
        fn = fnHash[args.command]
        fn()
    else:
        print('Function %s not in function map:' % args.command)
        print("\t" + "\n\t".join( [fnName for fnName, fn in fnHash.items()] ))