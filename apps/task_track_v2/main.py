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

import work_unit
import render_html
import options
import serialization_json

_meta_shell_command = 'tt'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--regen_html', action='store_true')
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
        W = serialization_json.fromFile(dbFile)
    else:
        W = []

    W.append(workUnit)
    serialization_json.toFile(dbFile, W)

if __name__ == '__main__':
	dbFile = options.dbFile

	args = getArgs()
	if not args.regen_html:
		commandLineEnterWorkDone(dbFile)

	htmlFile = options.htmlFile
	wd = serialization_json.fromFile(dbFile)
	render_html.render(wd, htmlFile, options.dataFile)

