
import new_note

def testSimpleNoteTakingInsertsTime():
    note = open('./test/input/note_example.md').read()
    noteFilename = new_note.ingest(note, './test/output')
    content  = open(noteFilename).readlines()
    
    expect = 'time::'
    for line in lines:
        if len(line) > len(expect) and line[0:len(expect)] == expect:
            return
    raise Exception('Did not find time annotation.')

if __name__ == '__main__':
    testSimpleNoteTakingInsertsTime()
