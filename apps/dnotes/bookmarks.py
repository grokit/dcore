
import re


import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.meta as meta
import dcore.apps.dnotes.options as options

class Bookmark:

    def __init__(self, value):
        self.value = value
        self.url = None

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()

def _extract_bookmarks():
    note_files = util.get_all_note_files()

    bookmarks = []
    for ff in note_files:
        lines = open(ff, 'r').readlines()

        mark = 'item%sbookmark' % options.MSEP
        for line in lines:
            if mark in line:
                value = line.split(mark)[1].strip()
                if len(value)>0 and value[0] == ']': value = value[1:]
                if len(value)>0 and value[0] == ',': value = value[1:]
                value = value.strip()
                bm = Bookmark(value)
                match = re.search('(http[s]{0,1}://[^ ]*)', bm.value)
                if match is None:
                    match = re.search('(\w+/[^ ]*)', bm.value)
                if match is not None:
                    bm.url = match.group(1)

                bookmarks.append(bm)

    return bookmarks

################################################################################
# PUBLIC
################################################################################

def get_bookmarks_matching(query):
    """
    All strings in query need to present at some position in the bookmark.
    """
    assert type(query) == list

    bmarks = _extract_bookmarks()

    bmarks_filtered = []
    if len(query) == 0:
        bmarks_filtered = bmarks
    else:
        for bb in bmarks:
            matched = True
            for sq in query:
                if not (sq.lower() in bb.value.lower()):
                    matched = False
                    break
            if matched:
                bmarks_filtered.append(bb)

    return bmarks_filtered


