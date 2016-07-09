
import new_note

# Note as entered by user.
simpleNote = """
# Walk in the Park

tag::memories, fun

It was cloudy and nice. Like always!
"""

# Note as stored in ingest.md ready to be broken-down in files and folders.
simulatedIngestDotMd = """
# Walk the Dog

tag::memories, fun
time::2016-07-09 11:10

Remember to walk the dog tomorrow.

# Walk in the Park

time::2016-07-09 10:43

It was cloudy and nice. Like always!
"""

def testSimpleNoteTakingInsertsTime():
    
    noteFilename = new_note.ingest(simpleNote, './test/output')
    lines = open(noteFilename).readlines()
    
    expect = 'time::'
    for line in lines:
        if len(line) > len(expect) and line[0:len(expect)] == expect:
            return
    raise Exception('Did not find time annotation.')

if __name__ == '__main__':
    testSimpleNoteTakingInsertsTime()
