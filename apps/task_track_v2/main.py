"""
# TODO

OK  unit tests in their directories
OK:  separate serialization from class
- better html plot!!!! !!not-ascii!!!!not-ascii!!!!not-ascii!!- without this it!!not-ascii!!!!not-ascii!!!!not-ascii!!s pointless
- time in seattle time
- stats mode with UT in command line (look back past X days, concatenate on days)
"""

import argparse
import os
import webbrowser

import work_unit
import render_html
import options
import serialization_json

_meta_shell_command = 'tt'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--regen_html', action='store_true')
    parser.add_argument('-o', '--open', action='store_true')
    args = parser.parse_args()
    return args

class Test:
    def __init__(self):
        self.a = 1

def commandLineEnterWorkDone(dbFile):
    type = input('What category of work did you do?\n')
    length = float(input('How long did you work for (hours)?\n'))
    if length < 0: raise Exception('Invalid len: %f.' % length)
    comment = input('Comment?\n')
    workUnit = work_unit.WorkDone(type, length, comment)

    if os.path.isfile(dbFile):
        W = serialization_json.fromFile(dbFile)
    else:
        W = []

    W.append(workUnit)
    serialization_json.toFile(dbFile, W)

if __name__ == '__main__':
    dbFile = options.dbFile
    htmlFile = options.htmlFile

    args = getArgs()

    if args.open is True:
        webbrowser.open_new_tab(htmlFile)
        exit(0)

    if not args.regen_html:
        commandLineEnterWorkDone(dbFile)

    wd = serialization_json.fromFile(dbFile)
    render_html.render(wd, htmlFile, options.dataFile)


