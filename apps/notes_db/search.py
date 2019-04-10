"""
# TODO

This parses notes, and create Match based on query.
A more complete abstraction would be to parse a Note class, against which it is possible to filter by query and rank.
"""

import os
import argparse
import re
import math
import inspect

import dcore.apps.notes_db.data as data
import dcore.apps.notes_db.meta as meta

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

class ScorerLinesMentions:

    def __init__(self):
        self.total_score = 0

    def score(self, search_query, lines, fn_debug = False):
        bonus = 0

        # Bonus if mentionned a lot in file.
        nmention = 0
        for l in lines:
            match = re.search(search_query, l, re.IGNORECASE)
            if match is not None:
                nmention += 1

        if nmention > 0:
            if nmention > 10:
                nmention = 10
            bonus = 5 * (nmention / 20)

        if fn_debug:
            fn = inspect.stack()[0][3]
            print('%s: %s' % (fn, bonus))

        self.total_score += bonus

    def getScore(self):
        return self.total_score

def score(matches, search_query, fn_debug = False):
    """
    # TODO
    - Move to score.py
    """
    for m in matches:

        if fn_debug:
            print('scoring file: ', m.filename)

        scorers = []
        scorers.append(ScorerLinesMentions())

        with open(m.filename) as fh:
            i = 0
            lines = fh.readlines()

            # ::: do this automatically when process m, don't re-pass all lines
            metadata = meta.extract("\n".join(lines))

            # The flaw here is that this adds up infinitely with the number of lines.
            #score_linesMentions(search_query, lines, scores, fn_debug)
            for scorer in scorers:
                scorer.score(search_query, lines, fn_debug)

            # Bonus if in title, even better if towards beginning of file.
            lineMatchBonus = 0
            titleMatchBonus = 0
            for l in lines:
                match = re.search(search_query, l, re.IGNORECASE)

                multiplier = 1 - (i / len(lines))

                if match is not None:
                    level = titleLevel(l)

                    if level == 0:
                        lineMatchBonus += 1
                    else:
                        titleMatchBonus += multiplier * (2 + 5 * (4-titleLevel(l)) / 4.0)

            m.score += min(5, lineMatchBonus) + min(10, titleMatchBonus)

            # Bonus if match any tag, LARGE bonus if match uuid.
            uuidVerifyUnique = None
            for metad in metadata:
                if re.search(search_query, metad.value, re.IGNORECASE):
                    bonus = 5
                    if metad.metaType == 'uuid':
                        # Just sanity, uuid is meant to be unique per document.
                        assert uuidVerifyUnique is None
                        uuidVerifyUnique = metad.value
                        bonus *= 5

                    m.score += bonus

        for scorer in scorers:
            m.score += scorer.getScore()

        # MOVE to scorers! Why two patterns?
        # just pass lines
        #
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

        # enforce stable sort by inserting consistent but very small
        # score based on name
        t = 1
        for c in m.filename:
            t = (t * 7 + ord(c)) % 2**30 + 0.0001
        m.score += 1/t

def extractMatchSetsFromFiles(files, query, context_range):
    """
    Note: this returns a SET of matches, can be > 1 per file.
    """
    matches = []
    for filename in files:
        with open(filename) as fh:
            lines = fh.readlines()
            i = 0
            for l in lines:
                m = re.search(query, l, re.IGNORECASE)
                if m is not None:
                    g = m.group(0)
                    match = Match(filename, l) 

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

def manualSelect(matches, nCut = 30):

    print('Select an item by entering its corresponding number. Enter cancels.')
    i = 0

    if len(matches) > nCut:
        matches = matches[0:nCut]
        print('Too many matches, cutting down to %s.' % len(matches))

    for x in matches:
        print('%.2d (%.2f): %s' % (i, x.score, x.filename))
        i += 1

    s = input()
    if len(s) == 0: return None
    s = int(s)

    return matches[s]

def sortMatchesByScore(matches):
    return sorted(matches, key=lambda x: x.score, reverse=True)

def walkGatherAllFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append( os.path.join(dirpath, f) )
    return F

def getAllFiles():
    root = data.notesRoot()
    files = walkGatherAllFiles(root)
    files = [f for f in files if os.path.splitext(os.path.split(f)[1])[1] == '.md']
    files = [f for f in files if not '/archived' in os.path.split(f)[0]]
    return files

