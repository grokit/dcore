"""
Provide search and search + quick-action.

# TODO

## As

ns: if folder contains query: score UP.
ns: tag:::important should UP priority
- ns <x> should list if <x> is in filename or folder name (and not in file itself).

score: if it has has now tag: ++

. cdlast
directory of last note opened
. cdlast00 <-- last X

## Bs

nsd: go_to_dir_that_matches (e.g. file what matched in ns, would go to)
    -> better ns creates shortcut to last file matched

## Cs

task -n <name>: create
task -l: list
task <name> match and open
task -r <tack>: retires the task

recent: 10 last written to note files
file_task: append time if not there, 
vim: open at specific line
https://www.cyberciti.biz/faq/linux-unix-command-open-file-linenumber-function/
maybe instead of vimt, just have my pipe program that filters to valid filenames
break down spaces when searching in uuid, if ANY part of request in uuid => more points
when search in uuid, conside whole word match > regex. ex: one --> ::one-on-one, ::done
anything in a meh folder is disregarded

ns -> nt: new task. user inputs -> tasks/DATE_title with tag:;:task

Color in results. http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

## a more meaningful search

could break whole notes in set of words, then if I search two words not consecutively but in same note I can get a match
"""

import sys
import os
import argparse
import re
import math

import dcore.apps.notes_db.data as data
import dcore.apps.notes_db.meta as meta 
import dcore.apps.notes_db.search as search

# ns: Note Search
_meta_shell_command = 'ns'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('search_query', nargs='+')
    parser.add_argument('-c', '--context_range', nargs = '?', type=int, default = 5)
    parser.add_argument('-t', '--search_titles_only', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-m', '--match_infinite', action='store_true', help='If set, do not limit number of search results.')
    parser.add_argument('-s', '--search_only', action='store_true')
    parser.add_argument('-O', '--open_first_matching_file', action='store_true')

    # This is now sefault.
    #parser.add_argument('-o', '--open_matching_file', action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    G_ARGS = getArgs()
    query = " ".join(G_ARGS.search_query)

    files = search.getAllFiles()
    
    matches = search.searchInFiles(files, query, G_ARGS.context_range)
    if G_ARGS.search_titles_only:
        matches = [m for m in matches if isLineTitle(m.line)]

    search.score(matches, query, G_ARGS.verbose)

    matches = search.sortMatchesByScore(matches)

    if G_ARGS.search_only:
        for m in matches:
            if G_ARGS.context_range == 0:
                print(m.strAlone())
            else:
                print(m)
        sys.exit(0)

    dedup = {}
    for m in matches:
        dedup[m.filename] = m

    dedup_matches = []
    for k in dedup:
        dedup_matches.append(dedup[k])
    matches = dedup_matches
    matches = search.sortMatchesByScore(matches)

    if len(matches) == 0:
        print('Not opening since no file matched.')
        exit(0)

    selected = matches[0]
    if not G_ARGS.open_first_matching_file and len(matches) > 1:
        nCut = 30
        if G_ARGS.match_infinite:
            nCut = 1e9
        selected = search.manualSelect(matches, nCut)
    os.system("vi '%s'" % selected.filename)

