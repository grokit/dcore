"""
Provide search and search + quick-action.

# TODO

## As

- if a tag matches a folder name under articles, offer to merge (or tag `no-merge` if decide no)
    - list-tags
    - add-tags

- ns a b c
    -> will not find a c. Should split space and do search independently IN ADDITION to full search (which gets more points).

## Bs
## Cs

- ns -O :xtop --> open the most recent one if more than one match exactly

- keep track of how often open some files -- take into consideration in pick algorithm?

- ns open with vi at CORRECT LINE

- notes/articles/reading_notes/a_book -> folders {articles, reading_notes} should apply as tag. "non-root or leaf folders are tags"

ns: if folder contains query: score UP.
ns: tag:::important should UP priority
- ns <x> should list if <x> is in filename or folder name (and not in file itself).

. cdlast
directory of last note opened
. cdlast00 <-- last X

nhist -> list of opened or modified files inorder
    -> all opens go through some .py file which tracks metadata + fires up vi

BUG: only first # should count as a lot,
    # abc
    ...
    # def
    ... def should not get same points as abc.

- sort by modified, indicate by star in ns, option to open last mod

NOTE-db: list files by created + filesystem metadata

be able to see all documents authored and modified this week

- list and offer open by last disk write time

nsd: go_to_dir_that_matches (e.g. file what matched in ns, would go to)
    -> better ns creates shortcut to last file matched

- ns: be able to create rules, such as all articles tagged x should be moved under folder Y

- ns: tag:::something -> rule "all tags x should be under folder y"
        Ruleset:
        - notify if rules violated
        - offer to auto-fix (optional)

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

import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.meta as meta
import dcore.apps.dnotes.score as score
import dcore.apps.dnotes.search as search

# ns: Note Search
_meta_shell_command = 'ns'


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('search_query', nargs='*')
    parser.add_argument('-C',
                        '--context_range',
                        nargs='?',
                        type=int,
                        default=5)
    parser.add_argument('-t', '--search_tags', action='store_true')
    parser.add_argument(
        '-a',
        '--select_all',
        action='store_true',
        help=
        'Select all files in the gather phase (instead of filtering by regex).'
    )
    parser.add_argument('-m',
                        '--match_infinite',
                        action='store_true',
                        help='If set, do not limit number of search results.')
    parser.add_argument('-s', '--search_only', action='store_true')
    parser.add_argument('-O',
                        '--open_first_matching_file',
                        action='store_true')

    # This is now sefault.
    #parser.add_argument('-o', '--open_matching_file', action='store_true')
    return parser.parse_args()


def _manualSelect(matches, scores, nCut=30):

    print(
        'Select an item by entering its corresponding number. Enter cancels.')
    i = 0

    if len(matches) > nCut:
        matches = matches[0:nCut]
        print('Too many matches, cutting down to %s.' % len(matches))

    for i in range(len(matches)):
        print('%.2d (%.2f): %s' % (i, scores[i], matches[i].filename))

    s = input()
    if len(s) == 0: return None
    s = int(s)

    return matches[s]


def _dedupMatches(matches):
    dedup = {}
    for m in matches:
        dedup[m.filename] = m

    dedup_matches = []
    for k in dedup:
        dedup_matches.append(dedup[k])
    return dedup_matches


if __name__ == '__main__':
    G_ARGS = getArgs()

    query = ""
    if len(G_ARGS.search_query) > 0:
        query = " ".join(G_ARGS.search_query)

    if G_ARGS.select_all:
        query = '.*'

    assert len(query) > 0

    files = search.getAllFiles()

    # Use this to debug since files.
    if False:
        files0 = [f for f in files if 'folder/file1.md' in f]
        files1 = [f for f in files if 'folder/file2.md' in f]
        files = files0 + files1

    matches = search.extractMatchSetsFromFiles(files, query,
                                               G_ARGS.context_range)

    if G_ARGS.search_tags:
        matches = [m for m in matches if isLineTitle(m.line)]

    if G_ARGS.search_only:
        for m in matches:
            if G_ARGS.context_range == 0:
                print(m.strAlone())
            else:
                print(m)
        sys.exit(0)

    matches = _dedupMatches(matches)

    scores = []
    for match in matches:
        mscore = score.score(match, query)
        scores.append(mscore)

    matches, scores = search.sortMatchesByScore(matches, scores)

    if len(matches) == 0:
        print('Not opening since no file matched.')
        sys.exit(0)

    selected = matches[0]
    if not G_ARGS.open_first_matching_file and len(matches) > 1:
        nCut = 15
        if G_ARGS.match_infinite:
            nCut = 1e9
        selected = _manualSelect(matches, scores, nCut)
    os.system("vi '%s'" % selected.filename)
