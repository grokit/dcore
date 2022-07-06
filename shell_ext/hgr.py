"""
History Grep
"""

import sys
import os
import re
import argparse

_meta_shell_command = 'hgr'


def getArgs():
    parser = argparse.ArgumentParser()
    # https://docs.python.org/3/library/argparse.html#nargs
    parser.add_argument('regex', nargs='+')
    args = parser.parse_args()
    return args

def is_time_annotation_line(line):
    """
    Some shell are configured to add date/time, e.g.:
    #1656878732
    # 1656878732
    """
    line = line.strip()
    if line[0:1] == '#':
        line = line[1:].strip()
        if line.isnumeric():
            return True
    return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = getArgs()
        regex = " ".join(args.regex).strip()
    else:
        regex = '.*'

    lst = []
    lst_filtered = []
    already_seen = set()
    with open(os.path.expanduser('~/.bash_history'), 'r') as fh:
        for line in fh.readlines():
            line = line.strip()
            mm = re.search(regex, line)
            if mm is not None:
                #print(line)
                #print(mm.group(0))
                lst.append(line)

    for i in range(len(lst)-1, -1, -1):
        if lst[i] not in already_seen:
            lst_filtered.append(lst[i])
            already_seen.add(lst[i])
    lst_filtered.reverse()

    for ll in lst_filtered:
        if not is_time_annotation_line(ll):
            print(ll)
