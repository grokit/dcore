"""
"""

import sys
import os
import argparse
import re
import webbrowser
import math

import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.meta as meta
import dcore.apps.dnotes.score as score
import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.bookmarks as bookmarks

_meta_shell_command = 'book'


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('search_query', nargs='*')
    parser.add_argument(
        '-O',
        '--open_first',
        action='store_true',
        help=
        'Try to open website in browser.'
    )
    return parser.parse_args()

if __name__ == '__main__':
    G_ARGS = getArgs()

    bmarks = bookmarks.get_bookmarks()

    bmarks_filtered = []

    if G_ARGS.search_query == []:
        bmarks_filtered = bmarks
    else:
        for bb in bmarks:
            for sq in G_ARGS.search_query:
                if sq.lower() in bb.value.lower():
                    bmarks_filtered.append(bb)
                break

    for bb in bmarks_filtered:
        print(bb)

    if G_ARGS.open_first and len(bmarks_filtered) > 0:
        bb = bmarks_filtered[0]
        print('Open browser for url: %s.' % bb.url)
        webbrowser.open_new_tab(bb.url)



