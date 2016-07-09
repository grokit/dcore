"""
Transform a flat note file to directories.
"""

import re

class Note:

    def fromText(note):
        note = Note()
        return note

    def writeSelf(self):
        pass

def ingest(filename):
    # Keep a copy just in case.
    open(filename + '.delme', 'w').write(open(filename).read())

    content = open(filename).readlines()

    notes = splitFlatFileInNoteChunck(filename)

    for note in notes:
        objNote = Note.fromText(note)
        objNote.writeSelf()

    # Clear file
    open(filename, 'w').write('\n')

def splitFlatFileInNoteChunck(noteContent):

    lines = noteContent.splitlines()

    buf = []
    for line in lines:
        buf.append(line)

    asStr = "\n".join(buf)
    yield asStr


if __name__ == '__main__':
    pass
