"""
Transform a flat note file to directories.

# TODO

- !! should still be able to ingest specific file -> if just file, create a default folder with file and filename as title with appropriate tag

- Auto do it from any folder.
- Before and after: commit to git

# BUGS
"""

import os
import hashlib
import time
import datetime
import argparse

import data
import util
import meta

import options

_meta_shell_command = 'ingest'

TITLE_SAFE_CHARSET = set('abcdefghijklmnopqrstuvwxyz-_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

TIME_FORMAT = '%Y-%m-%d_%H:%M'

# Putting back minutes so that notes of the day are ordered.
#TIME_FORMAT_FOLDER_NAME = '%Y-%m-%d'
TIME_FORMAT_FOLDER_NAME = TIME_FORMAT.replace(":", "-")

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
    def fromText(noteMd):
        note = Note()

        title = None
        unixTime = None

        note.meta = meta.metaToDict(meta.extract(noteMd))

        if 'time' in note.meta:
            if unixTime is None:
                unixTimeStr = note.meta['time']
                assert len(unixTimeStr) == 1
                unixTimeStr = list(unixTimeStr)[0]
                unixTime = timeStrToUnixTime(unixTimeStr)
            else:
                print('Multiple time tag per entry.', title)

        lines = noteMd.splitlines()
        for line in lines:
            # Title is the first leading-pound of the note.
            potTitle = detectTitle(line)
            if title is None and potTitle is not None:
                title = potTitle

        if title is None:
            h = hashlib.new('sha256')
            h.update(noteMd.encode())
            title = 'Anonymous-Note-%s' % h.hexdigest()[0:8]

        # User did not use automatic tool for unixTime, insert unixTime of ingestion.
        if unixTime is None:
            unixTime = time.time() 
            tag = ('\n\ntime%s' % options.MSEP) + unixTimeAsSafeStr(unixTime)
            noteMd = noteMd + tag

        note.title = title
        note.unixtime = unixTime
        note.content = noteMd
        return note

    def tags(self):
        if 'tag' not in self.meta:
            return set()
        return self.meta['tag']

    def writeSelf(self, folderOut):
        topFolderName = toFolderName(self.title, self.unixtime)
        folderWriteTo = os.path.join(folderOut, topFolderName)

        while os.path.exists(folderWriteTo):
            print('Warning: `%s` already exist, picking next folder.' % folderWriteTo)
            folderWriteTo = folderWriteTo + '_'

        fileWriteTo = os.path.join(folderWriteTo, 'note.md')
        os.makedirs(folderWriteTo)

        with open(fileWriteTo, 'w') as fh:
            print('Wrote note titled `%s` to `%s`.' % (self.title, fileWriteTo))
            fh.write(self.content)

def splitFlatFileInNoteChunck(lines):
    """
    # Note1

    Content1

    #

    Content 2

    # Note3

    Content 3

    Expected: yield 3 notes, second one with empty title.
    """
    assert type([]) == type(lines)

    buf = []
    potTitle = None
    for line in lines:
        newTitle = detectTitle(line)
        if newTitle != None and potTitle == None:
            potTitle = newTitle
        elif newTitle != None and potTitle != None:
            # We have two titles, can write completed section.
            asStr = "".join(buf)
            yield asStr

            buf = []
            potTitle = newTitle 
            newTitle = None
        buf.append(line)

    if len(buf) > 0:
        asStr = "".join(buf)
        yield asStr

def backupFileToBeIngested(filename, folderOut, contentLines):
    saveFolder = folderOut

    util.createFolderIfNotExist(saveFolder)
    content = "".join(contentLines)
    h = hashlib.new('sha256')
    h.update(content.encode())
    unixTime = time.time() 
    timeTag = unixTimeAsSafeStr(unixTime)
    saveFile = os.path.join('ingest.%s.%s.processed' %  (timeTag, h.hexdigest()[-16:]))
    saveFile = os.path.join(saveFolder, saveFile)

    with open(saveFile, 'w') as fh:
        print('Saving ingested data at `%s`.' % saveFile)
        fh.write(content)

def ingest(folderOut, contentLines):

    notes = splitFlatFileInNoteChunck(contentLines)

    processedLoc = folderOut
    for note in notes:
        objNote = Note.fromText(note)

        if 'merge' in objNote.tags():
            # Do not handle this scenario yet...
            pass

        objNote.writeSelf(processedLoc)

    return processedLoc

def getArgs():
    parser = argparse.ArgumentParser()
    # nargs = ? -> optional, if not will throw error when user does
    # not provide default.
    # parser.add_argument('file', default = 'ingest.md', nargs = '?')
    return parser.parse_args()


def gitCommit(folder, message):
    os.chdir(folder)
    os.system('git add -A')
    message = message.replace('"', '_')
    message = message.replace("'", '_')
    os.system("git commit -m '%s'" % message)

def preChangeHook():
    folderOut = data.notesRoot()
    gitCommit(folderOut, "%s_preChangeHook" % __file__)

def postChangeHook():
    folderOut = data.notesRoot()
    gitCommit(folderOut, "%s_postChangeHook" % __file__)

if __name__ == '__main__':
    args = getArgs()

    preChangeHook()

    folderOut = data.notesRoot()
    filename = data.ingestFilename(folderOut)

    contentLines = open(filename).readlines()

    backupFileToBeIngested(filename, os.path.join(folderOut, 'backups'), contentLines)
    ingest(os.path.join(folderOut, 'notes/low'), contentLines)
    os.remove(filename)

    postChangeHook()

