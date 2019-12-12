"""
Score matches in a sensible way for our dear user.

This needs some refactoring.
"""

import re
import os
import time
import math
import pathlib

import dcore.apps.notes_db.meta as meta

DEBUG = False

class ScorerLinesMentions:
    """
    One of N scorers.
    """

    def __init__(self):
        self.total_score = 0

    def score(self, search_query, lines):
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

        if DEBUG:
            fn = inspect.stack()[0][3]
            print('%s: %s' % (fn, bonus))

        self.total_score += bonus

    def getScore(self):
        return self.total_score

def _lastModified(filename):
    mtime = pathlib.Path(filename).stat().st_mtime
    return mtime

def isLineTitle(line):
    if len(line) > 1 and line[0] == '#':
        return True
    return False

def _titleLevel(line):
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

def score(match, search_query):

    match_score = 0

    if DEBUG:
        print('scoring file: ', match.filename)

    scorers = []
    scorers.append(ScorerLinesMentions())

    with open(match.filename) as fh:
        i = 0
        lines = fh.readlines()

        # TODO: do this automatically when process m, don't re-pass all lines
        metadata = meta.extract("\n".join(lines))

        # The flaw here is that this adds up infinitely with the number of lines.
        #score_linesMentions(search_query, lines, scores, DEBUG)
        for scorer in scorers:
            scorer.score(search_query, lines)

        # Bonus if in title, even better if towards beginning of file.
        lineMatchBonus = 0
        titleMatchBonus = 0
        for l in lines:
            rmatch = re.search(search_query, l, re.IGNORECASE)

            multiplier = 1 - (i / len(lines))

            if rmatch is not None:
                level = _titleLevel(l)

                if level == 0:
                    lineMatchBonus += 1
                else:
                    titleMatchBonus += multiplier * (2 + 5 * (4-_titleLevel(l)) / 4.0)

        match_score += min(5, lineMatchBonus) + min(10, titleMatchBonus)

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

                match_score += bonus

    for scorer in scorers:
        match_score += scorer.getScore()

    # MOVE to scorers! Why two patterns?
    # just pass lines
    #
    # Some folder have special score.
    # /folder since /folder/ happens for last folder.
    if isLineTitle(match.line):
        match_score += 4
    if '/articles' in os.path.split(match.filename)[0]:
        match_score += 10
    if '/quality-b' in os.path.split(match.filename)[0]:
        match_score -= 5
    if '/low' in os.path.split(match.filename)[0]:
        match_score -= 10
    if '/done' in os.path.split(match.filename)[0]:
        match_score -= 15

    # Bonus if query matches anything in top level folder.
    folderName = os.path.split(match.filename)[0]
    if '/' in folderName:
        folderName = folderName.split('/')[-1]
        if re.search(search_query, folderName, re.IGNORECASE):
            match_score += 10

    # Based on time
    lastModified = _lastModified(match.filename)
    distFromNowDays = (time.time()-lastModified) / (60*60*24)
    assert distFromNowDays >= 0

    # solve for: e^(-x*365) = 0.5 -> -math.log(0.5)/365
    # This means that an item a year from now get score reduced by ~50%.
    correction = max(0.25, math.exp(-0.0018990333713971104 * distFromNowDays))

    if match_score < 0 and correction != 0:
        correction = 1/correction

    match_score *= correction

    # print(f'dist: {match.filename}: {distFromNowDays}, corr: {correction}, score: {match_score}')

    # enforce stable sort by inserting consistent but very small
    # score based on name
    t = 1
    for c in match.filename:
        t = (t * 7 + ord(c)) % 2**30 + 0.0001
    match_score += 1/t

    return match_score

