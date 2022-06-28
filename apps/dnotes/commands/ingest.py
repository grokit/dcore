"""
Ingest scratch file (notes/ingest.md) into a categorized note.

Usage:
    ingest .../notes/ingest.md
        - ingests the default scratch file
    ingest <loc>
        - infers from <loc> where the note should be ingested to
    ingest -f <file>
        - '' <file>

# Maybe?
- ingest -h : move ingested to cur dir
"""

import os
import hashlib
import time
import datetime
import argparse

import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.meta as meta
import dcore.apps.dnotes.options as options

_meta_shell_command = 'ingest'

TITLE_SAFE_CHARSET = set(
    'abcdefghijklmnopqrstuvwxyz-_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

TIME_FORMAT = '%Y-%m-%d_%H:%M'

# Putting back minutes so that notes of the day are ordered.
#TIME_FORMAT_FOLDER_NAME = '%Y-%m-%d'
TIME_FORMAT_FOLDER_NAME = TIME_FORMAT.replace(":", "-")

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('location_hint', nargs='*', default=None, help='Location hint for the folder does the note get created in (find best match based on a number of rules).')
    parser.add_argument('-o', '--output_folder', nargs=1, help='Specific output folder.')
    return parser.parse_args()


def timeStrToUnixTime(timeStr):
    dateObj = datetime.datetime.strptime(timeStr, TIME_FORMAT)
    return time.mktime(dateObj.timetuple())


def unixTimeAsSafeStr(unixTime):
    dt = datetime.datetime.fromtimestamp(unixTime)
    return dt.strftime(TIME_FORMAT)


def unixTimeAsSafeFolderStr(unixTime):
    "Use when attaching time to folder names."
    dt = datetime.datetime.fromtimestamp(unixTime)
    return dt.strftime(TIME_FORMAT_FOLDER_NAME)


def toFolderName(title, unixTime):
    buf = []
    for l in title:
        if l not in TITLE_SAFE_CHARSET:
            l = '-'
        buf.append(l.lower())
    safeTitle = "".join(buf)
    return unixTimeAsSafeFolderStr(unixTime) + '_' + safeTitle


def detectTitle(line):
    title = None
    if len(line) >= 2 and line[0] == '#' and line[1] != '#':
        title = line[1:].strip()
    return title


class Note:
    @staticmethod
    def fromText(note_fulltext):
        note = Note()

        title = None
        unixTime = None

        note.meta = meta.metaToDict(meta.extract(note_fulltext))

        if 'time' in note.meta:
            if unixTime is None:
                unixTimeStr = note.meta['time']
                assert len(unixTimeStr) == 1
                unixTimeStr = list(unixTimeStr)[0]
                unixTime = timeStrToUnixTime(unixTimeStr)
            else:
                print('Multiple time tag per entry.', title)

        lines = note_fulltext.splitlines()
        for line in lines:
            # Title is the first leading-pound of the note.
            potTitle = detectTitle(line)
            if title is None and potTitle is not None:
                title = potTitle

        if title is None:
            h = hashlib.new('sha256')
            h.update(note_fulltext.encode())
            title = 'anonymous note %s' % h.hexdigest()[0:8]

        # User did not use automatic tool for unixTime, insert unixTime of ingestion.
        if unixTime is None:
            unixTime = time.time()
            tag = ('\n\ntime%s' % options.MSEP) + unixTimeAsSafeStr(unixTime)
            note_fulltext = note_fulltext + tag

        note.title = title
        note.unixtime = unixTime
        note.content = note_fulltext
        return note

    def tags(self):
        if 'tag' not in self.meta:
            return set()
        return self.meta['tag']

    def writeSelf(self, folder_out):
        topFolderName = toFolderName(self.title, self.unixtime)
        folderWriteTo = os.path.join(folder_out, topFolderName)

        while os.path.exists(folderWriteTo):
            print('Warning: `%s` already exist, picking next folder.' %
                  folderWriteTo)
            folderWriteTo = folderWriteTo + '_'

        fileWriteTo = os.path.join(folderWriteTo, 'note.md')
        os.makedirs(folderWriteTo)

        with open(fileWriteTo, 'w') as fh:
            print('Wrote note titled `%s` to `%s`.' %
                  (self.title, fileWriteTo))
            fh.write(self.content)


def ingest(folder_out, contentLines):
    objNote = Note.fromText(contentLines)
    objNote.writeSelf(folder_out)


def gitCommit(folder, message):
    os.chdir(folder)
    os.system('git add -A')
    message = message.replace('"', '_')
    message = message.replace("'", '_')
    os.system("git commit -m '%s'" % message)


def preChangeHook():
    folder_out = data.get_notes_root_folder()
    gitCommit(folder_out, "%s_preChangeHook" % __file__)


def postChangeHook():
    folder_out = data.get_notes_root_folder()
    gitCommit(folder_out, "%s_postChangeHook" % __file__)


if __name__ == '__main__':
    args = getArgs()

    if args.output_folder:
        assert args.location_hint is None
        folder_out = args.output_folder
    elif args.location_hint:
        candidates = []
        if os.path.exists(data.get_notes_project_folder()):
            candidates += os.scandir(data.get_notes_project_folder())
        if os.path.exists(data.get_notes_articles_folder()):
            candidates += os.scandir(data.get_notes_articles_folder())

        sub = []
        for cand in candidates:
            if os.path.isdir(cand):
                sub += os.scandir(cand)
        candidates += sub

        candidates = [dir_entry.path for dir_entry in candidates]
        # ? check in which circumstances .path is not a folder ?
        candidates = [folder for folder in candidates if os.path.isdir(folder)]

        candidates = set(candidates)

        picked = []
        for cand in candidates:
            if '/' in cand:
                top_folder = cand.split('/')[-1]

            hint = " ".join(args.location_hint).strip()
            if hint in top_folder:
                picked.append(cand)

        if len(picked) == 0:
            print('No match found. Cancelling.')
            exit(0)

        if len(picked) > 1:
            print('Too many matches, select folder to ingest to:')
            picked = [util.manualSelect(picked)]

        folder_out = picked[0]

    else:
        folder_out = data.get_notes_low_folder()

    preChangeHook()

    fullpath = data.get_ingest_fullpath()

    content = open(fullpath).read()

    ingest(folder_out, content)
    os.remove(fullpath)

    postChangeHook()
