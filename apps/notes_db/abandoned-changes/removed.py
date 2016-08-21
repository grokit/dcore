"""
Place where unloved code come to hang-out with other unloved code and therefore becomes happy, loved code.



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




def markdownAddFileAsLink(mdfile, newfile):
    print(mdfile, newfile)
    annotation = '![](%s)' % os.path.relpath(newfile, os.path.split(mdfile)[0])
    
    fh = open(mdfile, 'r')
    fileContent = fh.read()
    fh = open(mdfile, 'w')
    fh.write('\n%s\n' % annotation + fileContent)


def renderInputBuf(fileAsArray):
    return "\n".join(fileAsArray).strip(STOP_MARKER) 

def appendContent(file, noteContent):
    fh = open(file, 'r')
    fileContent = fh.read()
    fh = open(file, 'w')
    fh.write(noteContent + '\n' + fileContent)
    
def getLatestScreenshotFilename():
    files = [os.path.join(screenshotFolder, f) for f in os.listdir(screenshotFolder)]
    files.sort(key=lambda x: os.path.getmtime(x))
    return os.path.abspath(files[-1])    







if platform.system() == 'Windows':
    screenshotFolder = r'C:\screenshots'
else:
    screenshotFolder = os.path.expanduser('~/Pictures')

parser.add_argument('-e', '--edit', action='store_true', default=False, help='Open target file (current note or scratch) in text editor.')
parser.add_argument('-x', '--explore_folder', action='store_true', default=False, help='Open journal folder in nautilus / explorer.')
parser.add_argument('-f', '--filename_copy_to_journal_directory', help='Copies the file to the journal current directory and inserts a link in the markdown file.')
parser.add_argument('-p', '--save_screenshot_to_current_journal', action='store_true', default=False, help="Copies latest file in screenshot directory and copies to folder which contains today's journal.")

if args.filename_copy_to_journal_directory:
    src = os.path.abspath(args.filename_copy_to_journal_directory)
    dst = os.path.abspath(os.path.join(journalOutputPath, os.path.split(args.filename_copy_to_journal_directory)[1]))
    
    if os.path.isfile(dst):
        raise Exception('Already a file at `%s`, not copying.' % dst)
    
    print('copy `%s` -> `%s`.' %(src, dst))
    shutil.copyfile(src, dst)
    markdownAddFileAsLink(file, dst)
    exit(0)

if args.save_screenshot_to_current_journal:
    src = getLatestScreenshotFilename()
    dst = os.path.abspath(os.path.join(journalOutputPath, os.path.split(src)[1]))
    
    if os.path.isfile(dst):
        raise Exception('Already a file at `%s`, not copying.' % dst)
    
    print('copy `%s` -> `%s`.' %(src, dst))
    shutil.copyfile(src, dst)
    markdownAddFileAsLink(file, dst)
    exit(0)
"""

import os
import shutil
import time

# Note as entered by user.
simpleNote = """
# Walk in the Park

tag::memories, fun

It was cloudy and nice. Like always!
"""

# Note as stored in ingest.md ready to be broken-down in files and folders.

time1 = '2016-02-03 11:10'
time2 = '2016-03-04 12:34'
simulatedIngestDotMd = """
# Walk the Dog

tag::memories, fun
time::%s

Remember to walk the dog tomorrow.

# Stroll in the Park

time::%s

It was cloudy and nice. Like always!

#

time::2014-01-01 10:10
Oh no, someone inserted an anonymous section (no title)!

# Eating a Cake

Yummmm but this does not contain time!
""" % (time1, time2)

preSection = """

Note in pre-section.
tag: f48fh309dj0913dj9j190dj029

# Post-Section Note

A note.
"""

noTitle = """

This is a very.

Careless.

Note.

Expect note to still be created with an anonymous title.

Tag: jd9d09j1290js1902js129nvsvns
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

    if os.path.exists(TEST_OUTPUT):
        shutil.rmtree(TEST_OUTPUT)

    if not os.path.exists(TEST_INPUT):
        os.makedirs(TEST_INPUT)

    filename = os.path.join(TEST_INPUT, 'ingest.md')
    fh = open(filename, 'w')
    fh.write(simulatedIngestDotMd)
    fh.close()

    loc = ingest.ingest(filename, TEST_OUTPUT)

    notesFolders = [f.split('_')[0] for f in os.listdir(loc)]
    print(notesFolders)

    assert time1.split(' ')[0] in notesFolders
    assert time2.split(' ')[0] in notesFolders

    # When no time is set in note, use current time.
    nowTimeAsFolderStr = ingest.unixTimeAsSafeStr(time.time()).split(' ')[0] 
    assert nowTimeAsFolderStr in notesFolders

    # Make sure that note that had no time now has time in it.
    notesFolders = [os.path.join(loc, f) for f in os.listdir(loc)]
    
    filename = None
    for nf in notesFolders:
        if nowTimeAsFolderStr in nf:
            assert filename is None
            filename = os.path.join(nf, 'note.md')
    
    with open(filename, 'r') as fh:
        content = fh.read()
        assert 'time::' in content

def testPreSection():
    import ingest

    if os.path.exists(TEST_OUTPUT):
        shutil.rmtree(TEST_OUTPUT)

    if not os.path.exists(TEST_INPUT):
        os.makedirs(TEST_INPUT)

    filename = os.path.join(TEST_INPUT, 'pre-section.md')
    fh = open(filename, 'w')
    fh.write(preSection)
    fh.close()

    loc = ingest.ingest(filename, TEST_OUTPUT)

    notesFolders = [os.path.join(loc, f) for f in os.listdir(loc)]
    assert len(notesFolders) == 1

    with open(os.path.join(notesFolders[0], 'note.md')) as fh:
            content = fh.read()
            assert 'f48fh309dj0913dj9j190dj029' in content

def testNoTitle():
    import ingest

    if os.path.exists(TEST_OUTPUT):
        shutil.rmtree(TEST_OUTPUT)

    if not os.path.exists(TEST_INPUT):
        os.makedirs(TEST_INPUT)

    filename = os.path.join(TEST_INPUT, 'no-title.md')
    fh = open(filename, 'w')
    fh.write(noTitle)
    fh.close()

    loc = ingest.ingest(filename, TEST_OUTPUT)

    notesFolders = [os.path.join(loc, f) for f in os.listdir(loc)]
    assert len(notesFolders) == 1

    with open(os.path.join(notesFolders[0], 'note.md')) as fh:
            content = fh.read()
            assert 'jd9d09j1290js1902js129nvsvns' in content

def testPoundIsFirst():
    import ingest

    if os.path.exists(TEST_OUTPUT):
        shutil.rmtree(TEST_OUTPUT)

    if not os.path.exists(TEST_INPUT):
        os.makedirs(TEST_INPUT)

    poundFirst = """# The title

    the content
    """

    filename = os.path.join(TEST_INPUT, 'ingest.md')
    fh = open(filename, 'w')
    fh.write(poundFirst)
    fh.close()

    loc = ingest.ingest(filename, TEST_OUTPUT, poundFirst.splitlines())

    notesFolders = [f.split('_')[0] for f in os.listdir(loc)]
    print(notesFolders)


if __name__ == '__main__':
    #testSimpleNoteTakingInsertsTime()
    #testIngest()
    #testPreSection()
    #testNoTitle()
    testPoundIsFirst()

