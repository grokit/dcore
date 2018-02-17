"""
Get a daily digest of important, unclosed topics.
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

def getArgs():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

def do():
    args = getArgs()
    query = "todo%sa" % (':'*3)

    files = search.getAllFiles()
    
    context_range = 7
    matches = search.searchInFiles(files, query, context_range)
    search.score(matches, query)

    matches = search.sortMatchesByScore(matches)
    T = []
    for m in matches:
        T.append('~'*80 + '\n')
        T.append(m.strWithLine())
    t = "".join(T)
    
    title = "Digest R9uO6Eje %s" % (dateForAnnotation())
    content = t
    gmail.sendEmail(private_data.primary_email, title, content)


if __name__ == '__main__':
    do()
