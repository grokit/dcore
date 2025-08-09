"""
This parses notes, and create Match based on query.
A more complete abstraction would be to parse a Note class, against which it is possible to filter by query and rank.
"""

import os
import time
import argparse
import re
import math
import inspect
import pathlib
import datetime

import dcore.dcolor as dcolor

import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.meta as meta
import dcore.kvp_store as kvp_store

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

class __MetaValueAll: 
    """
    Just a marker meaning we only care about keys.
    """
    pass

def get_filenames_matching_meta_key_and_value(meta_key, meta_value):
    """
    E.g. key: uuid, value: 123456789
    """
    files = util.get_all_note_files()

    files_and_lines_matching = []
    for ff in files:
        metas = meta.extract(ff, open(ff).read())
        for mm in metas:
            if mm.meta_type == meta_key and (type(meta_value) == __MetaValueAll  or mm.value == meta_value):
                filename = mm.source_filename
                line_no = mm.line_no
                files_and_lines_matching.append((filename, line_no))

    return files_and_lines_matching

def get_filenames_matching_meta_key(meta_key):
    return get_filenames_matching_meta_key_and_value(meta_key, __MetaValueAll())

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

def __grab_context(lines, i, context_range):
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

    return "\n".join(ctx)

def __search_chunk(query, lines, data, filename, context_range):
    matches = []

    query_chunk = query.split(' ')
    query_chunk = [qc.strip() for qc in query_chunk if len(qc) > 0]

    first_line_match = None
    context = None
    n_match = 0
    i_match = None
    # line is arbitrary in this case
    for chunk in query_chunk:
        if chunk in data:
            n_match += 1
            if first_line_match is None:
                i = 0
                for line in lines:
                    if chunk in line:
                        first_line_match = line
                        i_match = i
                    i += 1
                assert first_line_match is not None

    if n_match == len(query_chunk):
        assert first_line_match is not None
        match = Match(filename, first_line_match)
        assert i_match is not None
        match.context = __grab_context(lines, i_match, context_range)
        matches.append(match)

    return matches

def __extractMatchSetsFromFiles_SingleFile(query, filename, lines, data, context_range):
    """
    Idea: the type of match should matter in scoring: at random place in file
    is not as good as all in the same line.

    todo:::c1 __grab_context(...) is BAD. Instead, just carry (i_line, filename), avoid
    copy all those strings and just grab when necessary (user request).
    """

    matches = []
    # We could extract and store Meta here. We don't, and do it 
    # on demand later if necessary.
    i = 0
    if len(query.strip()) == 0:
        matches.append(Match(filename, ""))
        return matches

    # when searching line by line, can you satisfy query
    for line in lines:
        match = None

        # regex
        if match is None:
            mm = re.search(query, line, re.IGNORECASE)
            if mm is not None:
                # This could both match regex as well as other for (filename, line)
                # ... this this is deduppe'd later on, so fine but could be improved.
                match = Match(filename, line)
                match.context = __grab_context(lines, i, context_range)

        # straight string matching
        if match is None:
            query_chunk = query.split(' ')
            query_chunk = [qc.strip() for qc in query_chunk if len(qc) > 0]
            n_match = 0
            for qc in query_chunk:
                if qc in line:
                    n_match += 1
            if n_match == len(query_chunk):
                match = Match(filename, line)
                match.context = __grab_context(lines, i, context_range)

        if match is not None:
            matches.append(match)

        i += 1

    # when searching in the whole file, can you satisfy query
    matches += __search_chunk(query, lines, data, filename, context_range)

    out = []
    seen = set()
    for mm in matches:
        key = (mm.filename, mm.line)
        if key not in seen:
            seen.add(key)
            out.append(mm)
    matches = out
    return matches


def extractMatchSetsFromFiles(files, query, context_range = 5):
    """
    Note: returns a SET of MATCHES, can be > 1 per file.
    """
    s_time = time.perf_counter()
    matches = []
    if len(files) == 0:
        return matches
    for filename in files:
        with open(filename) as fh:
            data = fh.read()
        lines = data.splitlines()
        matches += __extractMatchSetsFromFiles_SingleFile(query, filename, lines, data, context_range)
    e_time = time.perf_counter()
    time_us = (e_time - s_time)*(1000*1000)
    time_per_file = time_us / len(files)
    msg = f'took {time_per_file:.2f}us per file searching {len(files)} files, total {time_us/1000:.2f}ms'
    print(msg)
    kvp_store.write(f'{str(datetime.date.today()).replace("-","_")}/v{util.version().replace(".", "_")}/search_stat/{int(1000*time.time())}', msg, namespace='ns_search_stats')
    return matches
