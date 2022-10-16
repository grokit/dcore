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

import dcore.dcolor as dcolor

import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.meta as meta


class Match:
    def __init__(self, filename, lineContent):
        self.filename = filename
        self.line = lineContent
        self.last_mod_unixseconds = os.path.getmtime(self.filename)

        # Lines around the match (optional).
        self.context = None

    def strWithLine(self):
        content = self.line
        if self.context is not None:
            content = self.context

        return "%s\n%s" % (dcolor.green(self.filename), content)

    def strAlone(self):
        return self.line.strip()

    def matchAsOneLiner(self):
        return "%s\n%s" % (dcolor.green(self.filename), self.line.strip())

    def __str__(self):
        #return f'{self.filename}; {self.line[0:20]}...'
        return self.strWithLine()


################################################################################
# PUBLIC
################################################################################

def get_filenames_matching_meta(meta_key, meta_value):
    """
    E.g. key: uuid, value: 123456789
    """
    files = util.get_all_note_files()

    files_matching = []

    for ff in files:
        metas = meta.extract(ff, open(ff).read())
        for mm in metas:
            if mm.meta_type == meta_key:
                if mm.value == meta_value:
                    filename = mm.source_filename
                    files_matching.append(filename)

    return files_matching

def sortMatchesByScore(matches, scores, explanation=None):
    assert len(matches) == len(scores)
    if explanation is not None:
        assert len(matches) == len(explanation)
    else:
        explanation = ['']*len(matches)

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
            # We could extract and store Meta here. We don't, and do it 
            # on demand later if necessary.
            i = 0
            if len(query.strip()) == 0:
                matches.append(Match(filename, ""))
            else:
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
