"""
Provide search and search + quick-action.

# TODO

## As

Score depends on:
    Folder. Article = bonus.
    More points if mentioned more than once in filename

List of:
    Order (not score): time (newer better) for when score is ==.

## Bs

-i: only search documents tagged important
Color in results. http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

-t: use pre-defined (atom) text editor instead of vim

ns --list-tags
List all tags and popularity.
"""

import os
import argparse
import re
import math

import data

# ns: Note Search
_meta_shell_command = 'ns'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('search_query', nargs='+')
    parser.add_argument('-c', '--context_range', nargs = '?', type=int, default = 3)
    parser.add_argument('-t', '--search_titles_only', action='store_true')
    parser.add_argument('-o', '--open_matching_file', action='store_true')
    parser.add_argument('-O', '--open_first_matching_file', action='store_true')
    return parser.parse_args()

def walkGatherALlFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append( os.path.join(dirpath, f) )
    return F

class Match:

    def __init__(self, filename, lineContent):
        self.filename = filename
        self.line = lineContent
        self.score = 0

        # Lines around the match (optional).
        self.context = None

    def __str__(self):
        content = self.line
        if self.context is not None:
            content = self.context

        s = "%s (%s):\n%s" % (self.filename, self.score, content)
        return s

def score(matches):
    for m in matches:
        if isLineTitle(m.line):
            m.score += 4
        if '/articles/' in os.path.split(m.filename)[0]:
            m.score += 10
        if 'quality-b' in os.path.split(m.filename)[0]:
            m.score -= 5
        if '/low/' in os.path.split(m.filename)[0]:
            m.score -= 10

def searchInFiles(files):
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
                    cr = G_ARGS.context_range 
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

def manualSelect(items):

    print('Select an item by entering its corresponding number.')
    i = 0
    for x in items:
        print('%.1d: %s' % (i, x.filename))
        i += 1

    s = input()
    s = int(s)

    return items[s]

def sortMatches(matches):
    return sorted(matches, key=lambda x: x.score, reverse=True)

def getAllFiles():
    root = data.notesRoot()
    files = walkGatherALlFiles(root)
    files = [f for f in files if os.path.splitext(os.path.split(f)[1])[1] == '.md']
    return files

if __name__ == '__main__':
    G_ARGS = getArgs()
    print(G_ARGS)
    query = " ".join(G_ARGS.search_query)

    files = getAllFiles()
    
    matches = searchInFiles(files)
    if G_ARGS.search_titles_only:
        matches = [m for m in matches if isLineTitle(m.line)]
    score(matches)

    matches = sortMatches(matches)
    for m in matches:
        print(m)

    if G_ARGS.open_matching_file or G_ARGS.open_first_matching_file:
        dedup = {}
        for m in matches:
            dedup[m.filename] = m

        dedup_matches = []
        for k in dedup:
            dedup_matches.append(dedup[k])
        matches = dedup_matches
        matches = sortMatches(matches)

        if len(matches) == 0:
            print('Not opening since no file matched.')
            exit(0)

        selected = matches[0]
        if not G_ARGS.open_first_matching_file and len(matches) > 1:
            selected = manualSelect(matches)
        os.system('vim %s' % selected.filename)

