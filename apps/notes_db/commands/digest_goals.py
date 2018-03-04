"""
"""

_meta_shell_command = 'g_digest'

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

def getArgs():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

def render(query):
    files = search.getAllFiles()
    
    context_range = 200
    matches = search.searchInFiles(files, query, context_range)
    search.score(matches, query)

    matches = search.sortMatchesByScore(matches)
    T = []
    for m in matches:
        T.append('~'*80 + '\n')
        T.append(m.strWithLine())
    t = "".join(T)
    return t

def do():
    args = getArgs()

    cA = render("uuid%sgoals" % (':'*3))
    content = cA
    
    title = "Goals R97O6ejiKe %s" % (dateForAnnotation())
    gmail.sendEmail(private_data.primary_email, title, content)

if __name__ == '__main__':
    do()