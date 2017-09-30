"""
"""

import os
import argparse
import re
import math

import dcore.apps.notes_db.data as data
import dcore.apps.notes_db.meta as meta

def walkGatherALlFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append( os.path.join(dirpath, f) )
    return F

class Match:
    "TODO: move to ./classes"

    def __init__(self, filename, lineContent):
        self.filename = filename
        self.line = lineContent
        self.score = 0

        # Lines around the match (optional).
        self.context = None

    def strWithLine(self):
        content = self.line
        if self.context is not None:
            content = self.context

        s = "%s (%s):\n%s" % (self.filename, self.score, content)
        return s

    def strAlone(self):
        return self.line.strip()

    def __str__(self):
        return self.strWithLine()

def titleLevel(line):
    """
    titleLevel("# a title") -> 1
    titleLevel("## a title") -> 2
    titleLevel("### a title") -> 3
    titleLevel("#### a title") -> 4
    titleLevel("no markdown title") -> 0
    """

    level = 0
    if len(line) >= 1 and line[0] == '#':
        level += 1
    if len(line) >= 2 and line[1] == '#':
        level += 1
    if len(line) >= 3 and line[2] == '#':
        level += 1
    if len(line) >= 4 and line[3] == '#':
        level += 1

    return level

def score(matches, search_query):
    for m in matches:

        with open(m.filename) as fh:
            i = 0
            lines = fh.readlines()
            metadata = meta.extract("\n".join(lines))

            # Bonus if mentionned a lot in file.
            nmention = 0
            for l in lines:
                match = re.search(search_query, l, re.IGNORECASE)
                if match is not None:
                    nmention += 1

            if nmention > 0:
                if nmention > 20:
                    nmention = 20
                m.score += 5 * (nmention / 20)

            # Bonus if in title, even better if towards beginning of file.
            for l in lines:
                match = re.search(search_query, l, re.IGNORECASE)

                multiplier = 1 - (i / len(lines))

                if match is not None:
                    level = titleLevel(l)
                    if level != 0:
                        m.score += multiplier * (2 + 5 * (4-titleLevel(l)) / 4.0)

            # BIG bonus if query matches UUID.
            uuid = None
            for metad in metadata:
                if metad.metaType == 'uuid':
                    assert uuid is None
                    uuid = metad.value

            if uuid is not None and re.search(search_query, uuid, re.IGNORECASE):
                m.score += 8

        # Some folder have special score.
        # /folder since /folder/ happens for last folder.
        if isLineTitle(m.line):
            m.score += 4
        if '/articles' in os.path.split(m.filename)[0]:
            m.score += 10
        if '/quality-b' in os.path.split(m.filename)[0]:
            m.score -= 5
        if '/low' in os.path.split(m.filename)[0]:
            m.score -= 10
        if '/done' in os.path.split(m.filename)[0]:
            m.score -= 15

        # Bonus if query matches anything in top level folder.
        folderName = os.path.split(m.filename)[0]
        if '/' in folderName:
            folderName = folderName.split('/')[-1]
            if re.search(search_query, folderName, re.IGNORECASE):
                m.score += 10

def searchInFiles(files, query, context_range):
    matches = []
    for f in files:
        with open(f) as fh:
            lines = fh.readlines()
            i = 0
            for l in lines:
                m = re.search(query, l, re.IGNORECASE)
                if m is not None:
                    g = m.group(0)
                    match = Match(f, l) 

                    ctx = []
                    cr = context_range 
                    if cr % 2 == 1:
                        # Since -3//2 = 2 and not 1.
                        cr -= 1

                    for r in range(-cr//2, cr//2+1, 1):
                        if i + r >= 0 and i + r < len(lines):
                            if r == 0:
                                ctx.append('**  ' + lines[i+r])
                            else:
                                ctx.append('    ' + lines[i+r])

                    match.context = "".join(ctx)
                    matches.append(match)
                i += 1
    return matches

def isLineTitle(line):
    if len(line) > 1 and line[0] == '#':
        return True
    return False

def manualSelect(matches):

    print('Select an item by entering its corresponding number. Enter cancels.')
    i = 0
    for x in matches:
        print('%.1d (%.2f): %s' % (i, x.score, x.filename))
        i += 1

    s = input()
    if len(s) == 0: return None
    s = int(s)

    return matches[s]

def manualSelectSimple(matches):

    print('Select an item by entering its corresponding number. Enter cancels.')
    i = 0
    for x in matches:
        print('%.1d: %s' % (i, x))
        i += 1

    s = input()
    if len(s) == 0: return None
    s = int(s)

    return matches[s]

def sortMatchesByScore(matches):
    return sorted(matches, key=lambda x: x.score, reverse=True)

def getAllFiles():
    root = data.notesRoot()
    files = walkGatherALlFiles(root)
    files = [f for f in files if os.path.splitext(os.path.split(f)[1])[1] == '.md']
    files = [f for f in files if not '/archived' in os.path.split(f)[0]]
    return files

