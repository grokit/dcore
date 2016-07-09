"""
Transform a flat note file to directories.
"""

import re
import datetime

TITLE_SAFE_CHARSET = set('abcdefghijklmnopqrstuvwxyz-_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def timeStrToUnixTime(timeStr):
    # @@@@@TODO
    return 0

def unixTimeAsSafeStr(unixTime):
    dt = datetime.fromtimestamp(unixTime)
    return dt.strftime("%Y-%m-%d")    

def toFolderName(title, unixTime):
    buf = []
    for l in title:
        if l not in TITLE_SAFE_CHARSET:
            l = '-'
        buf.append(l)
    safeTitle = "".join(buf)
    return unixTimeAsSafeStr(unixtime) + '_' + safeTitle

# @@TODO: move to note.py 
# @@TODO: separate serialization from object repr (note_serialization.py)
class Note:

    def fromText(noteMd):
        note = Note()

        title = None
        time = None
        lines = noteMd.splitlines()
        # @@TODO: hadle tags to make searcheable
        for line in lines:
            # Title is the first leading-pound of the note.
            if time is None and len(line) >= 2 and line[0] == '#' and line[1] != '#':
                title = line[1:].strip()

            if 'time::' in line:
                assert time is None
                timeStr = line.split('time::')[1]
                time = timeStrToUnixTime(timeStr)

        assert title is not None
        # @@ if time is none insert now
        assert time is not None

        note.title = title
        note.unixtime = time
        note.content = nodeMd
        return note

    def writeSelf(self, folderOut):
        topFolderName = toFolderName(self.title, self.unixtime)
        folderWriteTo = os.path.join(folderOut, toFolderName)
        fileWriteTo = os.path.join(folderWriteTo, 'note.md')

        assert not os.path.exists(folderWriteTo)
        os.makedirs(folderWriteTo)

        with open(fileWriteTo, 'w') as fh:
            fh.write(note.content)

def ingest(filename, folderOut):
    # Keep a copy just in case.
    open(filename + '.delme', 'w').write(open(filename).read())

    contentLines = open(filename).readlines()

    notes = splitFlatFileInNoteChunck(contentLines)

    for note in notes:
        objNote = Note.fromText(note)
        objNote.writeSelf(folderOut)

    # Clear file
    open(filename, 'w').write('\n')

def splitFlatFileInNoteChunck(lines):
    assert type([]) == type(lines)

    buf = []
    for line in lines:
        buf.append(line)

    asStr = "\n".join(buf)
    yield asStr


if __name__ == '__main__':
    pass
