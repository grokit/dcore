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

    bmarks = bookmarks.get_bookmarks_matching(G_ARGS.search_query)
    for bb in bmarks:
        print("\n%s"%bb)

    if G_ARGS.open_first and len(bmarks) > 0:
        bb = bmarks[0]
        print('Open browser for url: %s.' % bb.url)
        webbrowser.open_new_tab(bb.url)



