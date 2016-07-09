
import os

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

TEST_OUTPUT = './test/output'
TEST_INPUT = './test/input'

def testSimpleNoteTakingInsertsTime():
    import new_note
    
    noteFilename = new_note.ingest(simpleNote, TEST_OUTPUT)
    lines = open(noteFilename).readlines()
    
    expect = 'time::'
    for line in lines:
        if len(line) > len(expect) and line[0:len(expect)] == expect:
            return
    raise Exception('Did not find time annotation.')

def testIngest():
    import ingest

    if not os.path.exists(TEST_INPUT):
        os.makedirs(TEST_INPUT)
    filename = os.path.join(TEST_INPUT, 'ingest.md')
    fh = open(filename, 'w')
    fh.write(simulatedIngestDotMd)
    fh.close()

    ingest.ingest(filename, TEST_OUTPUT)

if __name__ == '__main__':
    #testSimpleNoteTakingInsertsTime()
    testIngest()

