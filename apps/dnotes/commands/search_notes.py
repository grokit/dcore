"""
Provide search and search + quick-action.

- See luid:::ns_note_search_notes_018273_dcore_and_ideas_328744

# BUGS
- `engineering less` does not bring up lessons: engineering (since order different)
- word in title or uuid should rank higher
"""

import sys
import os
import argparse
import re
import math
import time

import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.meta as meta
import dcore.apps.dnotes.score as score
import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.options as options

# ns: note search
_meta_shell_command = 'ns'


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('search_query', nargs='*')
    parser.add_argument('-C',
                        '--context_range',
                        nargs='?',
                        type=int,
                        default=0)
    parser.add_argument('-n', '--number_of_matches_display', type=int, default=10)
    parser.add_argument(
        '-a',
        '--select_all',
        action='store_true',
        help=
        'Select all files in the gather phase (instead of filtering by regex).'
    )
    parser.add_argument('-e',
                        '--explain',
                        action='store_true',
                        help='If on, explain the score.')
    parser.add_argument('-t',
                        '--tag')
    parser.add_argument('-s', '--search_only', action='store_true')
    parser.add_argument('-O',
                        '--open_first_matching_file',
                        action='store_true')

    parser.add_argument('-u',
                        '--open_uuid',
                        help='Find an open file with corresponding unique id.')

    parser.add_argument('-f',
                        '--filter',
                        action='store_true',
                        help='WIP -- custom filters.')

    return parser.parse_args()


if __name__ == '__main__':
    G_ARGS = getArgs()


    query = ""
    if len(G_ARGS.search_query) > 0:
        query = " ".join(G_ARGS.search_query)

    if G_ARGS.select_all:
        query = '.*'

    # empty query == match all
    query = query.strip()

    files = util.get_all_note_files()

    open_first_matching_file = G_ARGS.open_first_matching_file
    if G_ARGS.open_uuid:
        query = 'uuid' + options.MSEP + G_ARGS.open_uuid
        open_first_matching_file = True

    matches = search.extractMatchSetsFromFiles(files, query, G_ARGS.context_range)

    if G_ARGS.search_only:
        # Do this BEFORE util.dedup_matches_to_one_per_file, otherwise, will not see when multiple matches
        # in the same file.
        for match in matches:
            if G_ARGS.context_range == 0:
                print(match.matchAsOneLiner())
                print('')
            else:
                print(match.strWithLine())
        sys.exit(0)

    matches = util.dedup_matches_to_one_per_file(matches)

    if G_ARGS.filter:
        print('WIP -- work in progress filters')
        matches = [mm for mm in matches if mm.last_mod_unixseconds >= time.time() - 24 * 60 * 60 * 1]

    if G_ARGS.tag:
        filtered = []
        for match in matches:
            metas = meta.extract(match.filename, open(match.filename, 'r').read())
            for meta_ in metas:
                if meta_.meta_type == 'tag' and meta_.value == G_ARGS.tag:
                    filtered.append(match)

        matches = filtered 

    scores = []
    explanations = []
    for match in matches:
        mscore, explanation = score.score(match, query, G_ARGS.explain)
        scores.append(mscore)
        explanations.append(explanation)

    matches, scores, explanations = search.sortMatchesByScore(
        matches, scores, explanations)

    if len(matches) == 0:
        print('Not opening since no file matched.')
        sys.exit(0)

    selected = matches[0]
    nCut = G_ARGS.number_of_matches_display

    if G_ARGS.explain:
        for i in range(0, nCut):
            if i < len(explanations):
                print(explanations[i])

    if not open_first_matching_file and len(matches) > 1:
        selected = util.manualSelectMatchesScores(matches, scores, nCut)

    util.openInEditor(selected.filename)
