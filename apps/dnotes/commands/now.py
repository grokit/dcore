"""
A shortlist of items tagged as now and/or pinned with nowa tag.

- tag `nowa`: gets priority. Use only that if any defined.
- tag `now`: fallback
- use -a option if want to use the union of both.
"""

import os
import argparse

import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.meta as meta
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.score as score

_meta_shell_command = 'now'

import sys

def getArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument('-a',
                        '--all',
                        action='store_true',
                        help='Return all in :now or :nowa, without distinction.')

    parser.add_argument('search_query', nargs='*')

    return parser.parse_args()

def get_by_tag(tag):
    files = util.get_all_note_files()

    files_matching = []

    for ff in files:
        metas = meta.extract(ff, open(ff).read())
        for mm in metas:
            if mm.meta_type == 'tag':
                if mm.value == tag:
                    filename = mm.source_filename
                    files_matching.append(filename)

    return files_matching


if __name__ == '__main__':
    args = getArgs()

    filenames = get_by_tag('nowa')

    if len(filenames) == 0 or args.all:
        filenames += get_by_tag('now')

    if not args.all:
        tmp = get_by_tag('now')
        if len(tmp) > 0:
            print('Ignoring the following given flags or presence of `nowa`:')
            for tt in tmp:
                print(f'\t{tt}')
            print('')

    query = ""
    if len(args.search_query) > 0:
        query = " ".join(args.search_query)

    matches = search.extractMatchSetsFromFiles(filenames, query)

    # can do this immediately (remove multiple matches per file)
    matches = util.dedup_matches_to_one_per_file(matches)

    scores = []
    for match in matches:
        mscore, _ = score.score(match, query, False)
        scores.append(mscore)

    matches, scores, _ = search.sortMatchesByScore(matches, scores)

    if len(matches) == 0:
        print('no match')
        exit(0)

    if len(matches) > 1:
        selected = util.manualSelectMatchesScores(matches, scores, int(1e9))
    else:
        selected = matches[0]

    util.openInEditor(selected.filename)


