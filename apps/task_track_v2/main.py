"""
# TODO
"""

import argparse
import os

import work_unit

def getArgs():

    parser = argparse.ArgumentParser()

    #parser.add_argument('-t', '--to', required=True)
    #parser.add_argument('subject', nargs='+')
    args = parser.parse_args()
    return args


class Test:

    def __init__(self):
        self.a = 1

def commandLineEnterWorkDone(dbFile):
    type = input('What category of work did you do?\n')
    length = float(input('How long did you work for (hours)?\n'))
    comment = input('Comment?\n')
    workUnit = work_unit.WorkDone(type, length, comment)

    if os.path.isfile(dbFile):
        W = work_unit.fromFile(dbFile)
    else:
        W = []

    W.append(workUnit)
    work_unit.toFile(dbFile, W)

if __name__ == '__main__':
    args = getArgs()
    dbFile = os.path.expanduser('~/sync/work_tracking_db.json')
    commandLineEnterWorkDone(dbFile)


