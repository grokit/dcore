"""
Open webpage showing stock
"""

_meta_shell_command = 'stock'

import argparse
import webbrowser

URL = 'https://finance.yahoo.com/chart/%s'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', default='none', nargs='?')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = getArgs()
    if args.command is not None:
        webbrowser.open(URL % args.command)
