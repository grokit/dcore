"""
Ingest scratch file (notes/ingest.md) into a categorized note.

Usage:
    ingest .../notes/ingest.md
        - ingests the default scratch file
    ingest <loc>
        - infers from <loc> where the note should be ingested to
    ingest -f <file>
        - '' <file>

# Ideas

- ingest should get a -f argument to swallow a file instead of the default one (ingest.md)
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

_TITLE_SAFE_CHARSET = set(
    'abcdefghijklmnopqrstuvwxyz-_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

_TIME_FORMAT = '%Y-%m-%d_%H:%M'
# Putting back minutes so that notes of the day are ordered.
_TIME_FORMAT_FOLDER_NAME = _TIME_FORMAT.replace(":", "-")

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('location_hint', nargs='*', default=None, help='Location hint for the folder does the note get created in (find best match based on a number of rules).')
    parser.add_argument('-o', '--output_folder', nargs=1, help='Specific output folder.')
    return parser.parse_args()


def timeStrToUnixTime(timeStr):
    dateObj = datetime.datetime.strptime(timeStr, _TIME_FORMAT)
    return time.mktime(dateObj.timetuple())


def unixTimeAsSafeStr(unixTime):
    dt = datetime.datetime.fromtimestamp(unixTime)
    return dt.strftime(_TIME_FORMAT)


def unixTimeAsSafeFolderStr(unixTime):
    "Use when attaching time to folder names."
    dt = datetime.datetime.fromtimestamp(unixTime)
    return dt.strftime(_TIME_FORMAT_FOLDER_NAME)


def toFolderName(title, unixTime):
    buf = []
    for l in title:
        if l not in _TITLE_SAFE_CHARSET:
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

        # maybe _unitTestsMetaToDict should only be used from UTs todo:::b1
        # ^^ replace with getting a fully typed
        note_meta = meta._unitTestsMetaToDict(meta.extract("fake.filename", note_fulltext))

        if 'time' in note_meta:
            if unixTime is None:
                unixTimeStr = note_meta['time']
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
            hh = hashlib.new('sha256')
            hh.update(note_fulltext.encode())
            title = 'anonymous note %s' % hh.hexdigest()[0:8]

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
            folderWriteTo = folderWriteTo + '_next'

        os.makedirs(folderWriteTo)
        fileWriteTo = os.path.join(folderWriteTo, 'note.md')

        with open(fileWriteTo, 'w') as fh:
            print('Wrote note titled `%s` to `%s`.' %
                  (self.title, fileWriteTo))
            fh.write(self.content)


def ingest_content(folder_out, contentLines):
    objNote = Note.fromText(contentLines)
    objNote.writeSelf(folder_out)


def gitCommit(folder, message):
    curr_dir = os.getcwd()
    os.chdir(folder)
    os.system('git add -A')
    message = message.replace('"', '_')
    message = message.replace("'", '_')
    os.system("git commit -m '%s'" % message)
    os.chdir(curr_dir)

def preChangeHook():
    folder_out = data.get_notes_root_folder()
    gitCommit(folder_out, "%s_preChangeHook" % __file__)


def postChangeHook():
    folder_out = data.get_notes_root_folder()
    gitCommit(folder_out, "%s_postChangeHook" % __file__)


def _find_output_folder(args):
    if args.output_folder:
        # oddly, it doesn't default to None as is indated but with an empty array
        assert len(args.location_hint) == 0
        assert len(args.output_folder) == 1
        folder_out = args.output_folder[0]
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

    assert folder_out is not None
    return folder_out

if __name__ == '__main__':
    args = get_args()

    preChangeHook()

    fullpath = data.get_ingest_fullpath()
    with open(fullpath, 'r') as fh:
        content = fh.read()

    folder_out = _find_output_folder(args)
    print(f'folder_out: {folder_out}')
    ingest_content(folder_out, content)

    os.remove(fullpath)

    postChangeHook()
