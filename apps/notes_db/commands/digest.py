"""
Get a daily digest of important, unclosed topics.

# TODO

- FIND a way to send on different schedule (FOREFRONT less often that TODO, etc)
- If A, B, C, D: Show A, B. If no A, show B, C. Etc (hide lower priorities).

"""

_meta_shell_command = 'n_digest'

import os
import datetime
import argparse
import platform
import shutil

import dcore.apps.notes_db.search as search
import dcore.apps.gmail.gmail as gmail
import dcore.private_data as private_data

def dateForAnnotation():
    return datetime.datetime.now().isoformat()

def render(query, context_range):
    files = search.getAllFiles()
    
    matches = search.extractMatchSetsFromFiles(files, query, context_range)
    search.score(matches, query)

    matches = search.sortMatchesByScore(matches)
    T = []
    for m in matches:
        T.append('~'*80 + '\n')
        T.append(m.strWithLine())
    t = "".join(T)
    return t

def doTODOsScatteredAndList():
    c0 = render("uuid%stodo" % (':'*3), 80)
    cA = render("todo%sa" % (':'*3), 10)
    cB = render("todo%sb" % (':'*3), 10)

    content = ""
    if len(c0 + cA+cB) != 0:
        content += c0
        content += "Scattered todos (As):\n"
        content += '-'*50 + '\n'
        content += cA
        content += '='*50 + '\n'
        content += "Scattered todos (Bs):\n"
        content += cB
    else:
        content += "No pending items, good job!\n"
    
    title = "Digest TODOs R9uO6Eje %s" % (dateForAnnotation())
    gmail.sendEmail(private_data.primary_email, title, content)

def doGoals():
    cA = render("uuid%sgoals" % (':'*3), 75)
    content = cA
    
    title = "Digest Goals R97O6ejiKe %s" % (dateForAnnotation())
    gmail.sendEmail(private_data.primary_email, title, content)

def doForefront():
    cA = render("uuid%sforefront" % (':'*3), 75)
    content = cA
    
    title = "Digest Forefront Oei8Jae %s" % (dateForAnnotation())
    gmail.sendEmail(private_data.primary_email, title, content)

def do():
    doGoals()
    doForefront()
    doTODOsScatteredAndList()

def test():
    cA = render("todo%sa" % (':'*3), 10)
    print(cA)

if __name__ == '__main__':
    do()
    #test()
