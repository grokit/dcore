"""
# TODO

- refactor so that there is just a list of function that are name-matched against arguments.
    - this way you can create 'shortcuts' to this.
    - can also list the possible mods
"""

import argparse

_meta_shell_command = 'textmod'


def getArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument('tomod', nargs='+')
    parser.add_argument('-m',
                        '--mode',
                        default='upper',
                        help='upper, lower, crazy, ascii, spaces')
    # maybe just have -a for ascii, etc

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = getArgs()
    print(args)

    txt = args.tomod

    if args.mode.lower() == 'fuzzmatch':
        txt = " ".join(args.tomod)
        toR = ['_', ' ']

        T = []
        for t in txt:
            if t in toR:
                T.append('.')
            else:
                T.append(t)
        txt = "".join(T)

    if args.mode.lower() == 'upper':
        txt = " ".join(args.tomod).upper()

    if args.mode.lower() == 'lower':
        txt = " ".join(args.tomod).lower()

    if args.mode.lower() == 'ascii':
        asc = []
        for x in " ".join(args.tomod):
            asc.append(str(ord(x)))
        txt = " ".join(asc)

    if args.mode.lower() == 'crazy':

        T = []
        txt = " ".join(args.tomod)
        for i in range(0, len(txt)):
            T.append(txt[i].lower() if i % 2 == 0 else txt[i].upper())
        txt = "".join(T)

    if args.mode.lower() == 'spaces':
        txt = " ".join(args.tomod)
        T = []
        for i in range(0, len(txt)):
            if i != 0:
                if txt[i].isupper() and not txt[i - 1].isupper():
                    T.append(' ')
                elif i != len(txt) - 2 and txt[i].isupper(
                ) and not txt[i + 1].isupper():
                    T.append(' ')
            T.append(txt[i])
        txt = "".join(T)

    print(txt)
