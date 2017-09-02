"""
# TODO

## As

-- tt -l <type>:
    list as kvp key: value, note[0:10]...

- Should be optional to have a unit (since sometimes just report mood or whatever).
    - last letter is digit -> number (float or int)
    - Should be able to specify units, e.g.:
        - 1 -> 1 hour (default interpretation)
        - 1m -> 1 minute
        - 1km -> 1 kilometer
        - 89h -> 89 on h scale
        --> basically letter qualifier after is saved
            interpretation is done. for things like hour min seconds, could input in any format but just keep in universal (seconds as float).

## Bs

- More generic plotting abilities. (react?). don't want to build all charts myself like I did with d3.


## Cs

- Mayyyybbbeee migrate to web project where can view and enter online under federated login. 

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
    parser.add_argument('-b', '--open_browser', action='store_true')
    parser.add_argument('-o', '--edit_db', action='store_true', help='Open database file with text editor.')
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

    if args.edit_db is True:
        cmd = 'vim %s' % options.dbFile
        print(cmd)
        os.system(cmd)
        exit(0)

    if args.open_browser is True:
        webbrowser.open_new_tab(htmlFile)
        exit(0)

    if not args.regen_html:
        commandLineEnterWorkDone(dbFile)

    wd = serialization_json.fromFile(dbFile)
    render_html.render(wd, htmlFile, options.dataFile)


