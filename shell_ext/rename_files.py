#!/usr/bin/python3
"""
Rename files / folders with nice, commonly used patterns.
"""

import re
import os
import argparse
import time

_meta_shell_command = 'rename_files'


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', nargs='?', default='remove_aggressive')
    parser.add_argument('rest', nargs='?')
    parser.add_argument('-t',
                        '--test',
                        action='store_true',
                        default=False,
                        help='Skip apply, just check what would happen.')
    parser.add_argument('-f', '--file', default=None)
    args = parser.parse_args()
    return args


def isNum(s):
    try:
        int(s)
    except:
        return False
    return True


def removeSpace(filename, args, state):
    to = re.sub('[ ()]', '_', filename)

    L = []
    for i in range(0, len(to)):
        if i != len(to) - 1:
            if isNum(to[i]) and not isNum(to[i + 1]):
                if i == 0 or not isNum(to[i - 1]):
                    L.append('0')
        L.append(to[i])
    to = ''.join(L)
    return to


def removeAggressive(filename, args, state):
    v = set(
        'abcdefghijklmnopqrstuvwxyz._-ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789[]'
    )  # ()

    accents_to_set = {
        'ä': 'a',
        'à': 'a',
        'â': 'a',
        '&': 'and',
        'é': 'e',
        'è': 'e',
        'ô': 'o',
        'ç': 'c',
        'Ä': 'A',
        'À': 'A',
        'Â': 'A',
        'É': 'E',
        'È': 'E',
        'Ô': 'O',
        'Ç': 'C',
    }

    toLower = True

    fout = []
    for l in filename:
        if l in v:
            fout.append(l)
        else:
            if l in accents_to_set:
                fout.append(accents_to_set[l])
            else:
                fout.append('_')

    if toLower:
        for i in range(0, len(fout)):
            fout[i] = fout[i].lower()

    ss = "".join(fout)
    while '__' in ss:
        ss = ss.replace('__', '_')
    while '_.' in ss:
        ss = ss.replace('_.', '.')
    return ss


def prefix(f, args, state):
    if arg is None:
        raise Exception('No country for None arg.')
    return "%s%s" % (arg, f)


def suffix(f, args, state):
    if arg is None:
        raise Exception('No country for None arg.')

    ext = ''
    if '.' in f:
        ext = f[f.rfind('.'):]
        f = f[:f.rfind('.')]

    return "%s_%s%s" % (f, arg, ext)


def date(f, args, state):
    t = time.strftime('%Y-%m-%d')
    return "%s_%s" % (t, f)


def custom(f, args, state):
    return f.replace('__', '_')

def sequence(f, args, state):
    """
    Rename files as 00.ext, ..., 09.ext.
    """

    _, ext = os.path.splitext(f)
    return '%.2i%s' % (state.i, ext)

def order_by(f, args, state):
    if '#' in f:
        n = int(f.split('#')[1].split('-')[0])
    else:
        n = 99
    return "%.2i_%s" % (n, f)


def change_ext(f, args, state):
    return os.path.splitext(f)[0] + '.markdown'

class State:

    def __init__(self):
        self.i = 0


if __name__ == '__main__':

    fnMap = {
        'remove_spaces': removeSpace,
        'remove_aggressive': removeAggressive,
        'change_ext': change_ext,
        'prefix': prefix,
        'suffix': suffix,
        'date': date,
        'sequence': sequence,
        'custom': custom,
        'order_by': order_by,
    }

    args = getArgs()
    mode = args.mode

    if args.file is not None:
        files = [args.file]
    else:
        files = os.listdir('.')
        #files = [f for f in files if os.path.isfile(f)]

    if mode not in fnMap:
        raise Exception('Error, mode not in map. Mode: %s, map: %s.' %
                        (mode, ", ".join(fnMap.keys())))

    print('Applying %s.' % mode)
    fn = fnMap[mode]

    state = State()
    for f in files:
        to = fn(f, args.rest, state)
        if f != to:
            print('%s -> %s' % (f, to))
            if not args.test:
                os.rename(f, to)
            else:
                print('Skipped since apply switch off.')
        state.i += 1
