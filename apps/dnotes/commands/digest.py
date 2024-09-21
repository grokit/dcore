"""
Get a daily digest of important, unclosed topics.

# TODO

- FIND a way to send on different schedule (FOREFRONT less often that TODO, etc)
- If A, B, C, D: Show A, B. If no A, show B, C. Etc (hide lower priorities).
"""

_meta_shell_command = 'nn_digest'

import os
import datetime
import argparse
import platform
import shutil

import dcore.apps.dnotes.options as options
import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.score as score
import dcore.utils as dutils


def render(query, context_range):
    files = search.getAllFiles()

    matches = search.extractMatchSetsFromFiles(files, query, context_range)
    scores = []
    explanations = []
    for match in matches:
        mscore, explanation = score.score(match, query, False)
        scores.append(mscore)
        explanations.append(explanation)

    matches, scores, explanation = search.sortMatchesByScore(
        matches, scores, explanations)

    T = []
    for m in matches:
        T.append('~' * 80 + '\n')
        T.append(m.strWithLine())
    t = "".join(T)

    return t


def doTODOsScatteredAndList():
    c0 = render("uuid%stodo" % options.MSEP, 80)
    cA = render("todo%sa" % options.MSEP, 10)
    cB = render("todo%sb" % options.MSEP, 10)

    content = ""
    if len(c0 + cA + cB) != 0:
        content += c0
        content += "Scattered todos (As):\n"
        content += '-' * 50 + '\n'
        content += cA
        content += '=' * 50 + '\n'
        content += "Scattered todos (Bs):\n"
        content += cB
    else:
        content += "No pending items, good job!\n"

    title = "Digest TODOs R9uO6Eje %s" % (dutils.date_now_for_annotation())
    return Message(title, content)


def doGoals():
    cA = render("uuid%sgoals" % (':' * 3), 75)
    content = cA

    title = "Digest Goals R97O6ejiKe %s" % (dutils.date_now_for_annotation())
    return Message(title, content)


def doForefront():
    cA = render("uuid%sforefront" % (':' * 3), 75)
    content = cA

    title = "Digest Forefront Oei8Jae %s" % (dutils.date_now_for_annotation())
    return Message(title, content)


class Message:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return "%s, %s" % (self.title, self.content)


def do():
    messages = []
    messages.append(doGoals())
    messages.append(doForefront())
    messages.append(doTODOsScatteredAndList())
    return messages


if __name__ == '__main__':
    messages = do()
    print(messages)
