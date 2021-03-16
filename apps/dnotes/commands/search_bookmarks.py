"""
# TODO

# As
- option -w: print filename that matched too
# Bs
# Cs

"""

import sys
import os
import argparse
import re
import webbrowser
import math

import dcore.dcolor as dcolor

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
    parser.add_argument(
        '-w',
        '--where',
        action='store_true',
        help=
        'Also print the file where the bookmark was found.'
    )
    return parser.parse_args()

if __name__ == '__main__':
    for i in range(80):
        print('')
    print('-'*60 + '````')
    G_ARGS = getArgs()

    bmarks = bookmarks.get_bookmarks_matching(G_ARGS.search_query)
    for bb in bmarks:

        where = ''
        if G_ARGS.where:
            where = '%s\n' % bb.fullpath_origin
            where = dcolor.green(where)
        print("\n%s%s"%(where, bb))

    if G_ARGS.open_first and len(bmarks) > 0:
        bb = bmarks[0]
        print('Open browser for url: %s.' % bb.url)
        webbrowser.open_new_tab(bb.url)



