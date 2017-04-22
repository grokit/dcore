"""
Provide search and search + quick-action.

# TODO

## As
## Bs

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
    parser.add_argument('-c', '--context_range', nargs = '?', type=int, default = 3)
    parser.add_argument('-t', '--search_titles_only', action='store_true')
    parser.add_argument('-o', '--open_matching_file', action='store_true')
    parser.add_argument('-O', '--open_first_matching_file', action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    G_ARGS = getArgs()
    query = " ".join(G_ARGS.search_query)

    files = search.getAllFiles()
    
    matches = search.searchInFiles(files, query, G_ARGS.context_range)
    if G_ARGS.search_titles_only:
        matches = [m for m in matches if isLineTitle(m.line)]
    search.score(matches, query)

    matches = search.sortMatchesByScore(matches)
    for m in matches:
        print(m)

    if G_ARGS.open_matching_file or G_ARGS.open_first_matching_file:
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
            selected = search.manualSelect(matches)
        os.system("vim '%s'" % selected.filename)
