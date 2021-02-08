"""
This parses notes, and create Match based on query.
A more complete abstraction would be to parse a Note class, against which it is possible to filter by query and rank.
"""

import os
import argparse
import re

import math
import inspect
import pathlib

import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.util as util


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

        return "%s:\n%s" % (self.filename, content)

    def strAlone(self):
        return self.line.strip()

    def matchAsOneLiner(self):
        # todo:::a1 RESUME: remove the "common path filename" if a common root in cwd
        return "%s: %s" % (self.filename, self.line.strip())


################################################################################
# PUBLIC
################################################################################


def sortMatchesByScore(matches, scores, explanation):
    assert len(matches) == len(scores)
    assert len(matches) == len(explanation)

    pairs = list(zip(matches, scores, explanation))
    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

    matches, scores, explanations = [[m for m, s, e in pairs],
                                     [s for m, s, e in pairs],
                                     [e for m, s, e in pairs]]

    return matches, scores, explanations


def extractMatchSetsFromFiles(files, query, context_range = 5):
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
