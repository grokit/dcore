"""
Provide search and search + quick-action.

- See luid:::ns_note_search_notes_018273_dcore_and_ideas_328744
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
import dcore.apps.dnotes.util as util

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
    parser.add_argument('--number_of_matches_display', type=int, default=5)
    parser.add_argument('-t', '--search_tags', action='store_true')
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

    if not G_ARGS.open_first_matching_file and len(matches) > 1:
        selected = _manualSelect(matches, scores, nCut)

    util.openInEditor(selected.filename)
