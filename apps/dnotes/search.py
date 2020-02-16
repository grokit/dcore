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
import pathlib

import dcore.apps.notes_db.data as data


class Match:
    def __init__(self, filename, lineContent):
        self.filename = filename
        self.line = lineContent

        # Lines around the match (optional).
        self.context = None

    def strWithLine(self):
        content = self.line
        if self.context is not None:
            content = self.context

        s = "%s:\n%s" % (self.filename, content)
        return s

    def strAlone(self):
        return self.line.strip()

    def __str__(self):
        return self.strWithLine()


def _walkGatherAllFiles(rootdir='.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append(os.path.join(dirpath, f))
    return F


################################################################################
# PUBLIC
################################################################################


def getAllFiles():
    root = data.notesRoot()
    files = _walkGatherAllFiles(root)
    files = [
        f for f in files if os.path.splitext(os.path.split(f)[1])[1] == '.md'
    ]
    files = [f for f in files if not '/archived' in os.path.split(f)[0]]
    return files


def sortMatchesByScore(matches, scores):
    assert len(matches) == len(scores)

    pairs = list(zip(matches, scores))
    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

    matches, scores = [[m for m, s in pairs], [s for m, s in pairs]]

    return matches, scores


def extractMatchSetsFromFiles(files, query, context_range):
    """
    Note: this returns a SET of matches, can be > 1 per file.
    """
    matches = []
    for filename in files:
        with open(filename) as fh:
            lines = fh.readlines()
            i = 0
            for line in lines:
                m = re.search(query, line, re.IGNORECASE)
                if m is not None:
                    g = m.group(0)
                    match = Match(filename, line)

                    ctx = []
                    cr = context_range
                    if cr % 2 == 1:
                        # Since -3//2 = 2 and not 1.
                        cr -= 1

                    for r in range(-cr // 2, cr // 2 + 1, 1):
                        if i + r >= 0 and i + r < len(lines):
                            if r == 0:
                                ctx.append('**  ' + lines[i + r])
                            else:
                                ctx.append('    ' + lines[i + r])

                    match.context = "".join(ctx)
                    matches.append(match)
                i += 1
    return matches
