"""
- Could also just set date and open in VIM.
"""

_meta_shell_command = 'journal'

import os
import datetime
import argparse

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--open', action='store_true', default=False, help='Just opens the file in text editor.')
    return parser.parse_args()

def date():
    return str(datetime.datetime.now()).split(' ')[0]

file = os.path.normpath(os.path.expanduser('~/journal.txt'))
stop = '!!!'

if __name__ == '__main__':

    args = getArgs()

    print('Using file: %s.' % file)

    if args.open:
        c = 'vim %s' % file
        print(c)
        os.system(c)
        exit(0)

    fh = open(file, 'r')
    print("Type '%s' to end." % stop)
    inputBuf = []
    while len(inputBuf) == 0 or inputBuf[-1].find(stop) == -1:
        try:
            lIn = input()
        except (EOFError):
            break
        if lIn == None:
            break # reached EOF
        inputBuf.append( lIn )

    inputBuf = ['# ' + date() + '\n'] + inputBuf

    fileContent = fh.read()
    fh = open(file, 'w')
    fh.write("\n".join(inputBuf).strip(stop) + '\n' + fileContent)
