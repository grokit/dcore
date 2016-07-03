"""
# Why

Make it easy to take, and later search, small notes from command line.

It removes hurdles that hinders quick note-taking:

    - Native to console, avoid having to switch to a UI application and works on all OS.
    - Fully scriptable (just 1 python script with no _forced_ dependencies).
    - Centralizes all notes to a folder, avoid having to `pushd.; cd ~/notes; take notes; popd;` everytime you want to take a note.
    - Append some metadata such as time of entry to notes.
    - Have convention for entering notes that make them easily searcheable by title or tags.

# Suggested Workflow

Take small notes using jl.

## Type a journal entry

    $ jl
    Here is my journal entry.
    :END

Note that the ':END' is a marker that you are done typing text. Until it is typed, the notes is not written to HD.
    
## Insert file as journal entry (directly in text file)
    
    $ jl < file

## Save a copy of file in same directory as journal
    
    $ jl -f filename
    
# IDEAS

## Maybe could make this more like an entry generator

- Everything goes in a daily folder.
- Text entries are just appended in a section of markdown document for the day (as link).
- Files are copied to the dir, with an automatic link inserted in markdown document (jl -f <filename>).
- If want to turn unto an article, just rename folder.
- Can add options for tags and cie.    
    
# TODO

- jl -c : store whatever is in clipboard as text

jl needs to be changed so that by default it writes to the blob and only when give proper title does it create new directory. then after one has been created make it easy to append to without send data to wo having to re-specify name

# BUGS

- scratch.markdown is one level too high.
"""

_meta_shell_command = 'jl'

import os
import datetime
import argparse
import platform
import shutil

# Todo: eventually have the curated notes and blog post also searcheable.
#       Think if that should be a different (search) script. Probably should (do one thing and one thing well).
otherNotesRoots = []

dataLocation = os.path.expanduser('~/notes')
try:
    # If you are using dcore system, take root from there.
    import dcore.data as data
    dataLocation = data.dcoreData()
except ImportError as e:
    pass

print('Using folder: %s.' % dataLocation)

stop = ':END'

if platform.system() == 'Windows':
    screenshotFolder = r'C:\screenshots'
else:
    screenshotFolder = os.path.expanduser('~/Pictures')

def dateForFile():
    return datetime.datetime.now().strftime("%Y-%m-%d")
    
def dateForFolder():
    return datetime.datetime.now().strftime("%Y-%m-%d")    
    
def dateForAnnotation():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list_interesting_meta', action='store_true', default=False, help='List manualy titled entries.')
    parser.add_argument('-o', '--open', action='store_true', default=False, help='Just opens the file in text editor.')
    parser.add_argument('-t', '--scratch', action='store_true', default=False, help="Use scratch-file instead of today's file (for stuff that is not really important, e.g. code snippets).")
    parser.add_argument('-e', '--explore_folder', action='store_true', default=False, help='Open journal folder in nautilus / explorer.')
    parser.add_argument('-f', '--filename_copy_to_journal_directory', help='Copies the file to the journal current directory and inserts a link in the markdown file.')
    parser.add_argument('-s', '--save_screenshot_to_current_journal', action='store_true', default=False, help="Copies latest file in screenshot directory and copies to folder which contains today's journal.")
    return parser.parse_args()

def markdownAddFileAsLink(mdfile, newfile):
    print(mdfile, newfile)
    annotation = '![](%s)' % os.path.relpath(newfile, os.path.split(mdfile)[0])
    
    fh = open(mdfile, 'r')
    fileContent = fh.read()
    fh = open(mdfile, 'w')
    fh.write('\n%s\n' % annotation + fileContent)

def annotateDate(file):
    fh = open(file, 'r')
    inputBuf = ['(time: ' + dateForAnnotation() + ')\n']
    fileContent = fh.read()
    fh = open(file, 'w')
    fh.write("\n".join(inputBuf).strip(stop) + '\n' + fileContent)

def appendContent(file, inputBuf):
    fh = open(file, 'r')
    fileContent = fh.read()
    fh = open(file, 'w')
    fh.write("\n".join(inputBuf).strip(stop) + '\n' + fileContent)
    
def getLatestScreenshotFilename():
    files = [os.path.join(screenshotFolder, f) for f in os.listdir(screenshotFolder)]
    files.sort(key=lambda x: os.path.getmtime(x))
    return os.path.abspath(files[-1])    
    
def do():    
    args = getArgs()

    if args.list_interesting_meta:
        """
        This is not com
        """

        journalOutputPath = dataLocation
        os.chdir(journalOutputPath)
        
        # Pound and date is inserted automatically, so skipped.
        # The really interesting information is what users tagged with a markdown style title.
        cmd = r'ag "^# [^0-9]"'
        print(cmd)
        os.system(cmd)

        # Also cool: tags. Right now this is really basic, could in the future do full-python search.
        cmd = r'ag "tag::"'
        print(cmd)
        os.system(cmd)
        exit(0)
    
    if args.scratch:
        journalOutputPath = dataLocation
        file = os.path.abspath(os.path.join(journalOutputPath, 'scratch.markdown'))
    else:
        journalOutputPath = os.path.abspath(os.path.join(dataLocation, 'journals/%s/' % dateForFolder()))
        
        if not os.path.exists(journalOutputPath):
            print('No such path `%s`, creating.' % journalOutputPath)
            os.makedirs(journalOutputPath)
            
        file = os.path.abspath(os.path.join(journalOutputPath, '%s_journal.markdown' % dateForFile()))
    
    print('Using file: %s.' % file)
    if not os.path.isfile(file):
        open(file, 'w').write("\n")
    
    if args.filename_copy_to_journal_directory:
        src = os.path.abspath(args.filename_copy_to_journal_directory)
        dst = os.path.abspath(os.path.join(journalOutputPath, os.path.split(args.filename_copy_to_journal_directory)[1]))
        
        if True:
            if os.path.isfile(dst):
                raise Exception('Already a file at `%s`, not copying.' % dst)
        
        print('copy `%s` -> `%s`.' %(src, dst))
        shutil.copyfile(src, dst)
        markdownAddFileAsLink(file, dst)
        exit(0)
    
    if args.save_screenshot_to_current_journal:
        src = getLatestScreenshotFilename()
        dst = os.path.abspath(os.path.join(journalOutputPath, os.path.split(src)[1]))
        
        if True:
            if os.path.isfile(dst):
                raise Exception('Already a file at `%s`, not copying.' % dst)
        
        print('copy `%s` -> `%s`.' %(src, dst))
        shutil.copyfile(src, dst)
        markdownAddFileAsLink(file, dst)
        exit(0)
    
    if args.explore_folder:
        if platform.system() == 'Windows':
            c = 'explorer %s' % journalOutputPath
        else:
            c = 'nautilus %s' % journalOutputPath
        print(c)
        os.system(c)
        exit(0)
        
    if args.open:
        annotateDate(file)
        if platform.system() == 'Windows':
            c = 'np %s' % file
        else:
            c = 'vim %s' % file
            #c = 'gedit %s' % file
            #c = 'kate %s' % file
        print(c)
        os.system(c)
        exit(0)
    
    print("Type your note, then '%s' to save and exit." % stop)
    inputBuf = []
    while len(inputBuf) == 0 or inputBuf[-1].find(stop) == -1:
        try:
            lIn = input()
        except (EOFError):
            break        
        if lIn == None:
            break # reached EOF
        inputBuf.append( lIn )

    # Since write from top, have to write content before date if want date as header.
    appendContent(file, inputBuf)
    annotateDate(file)
    
if __name__ == '__main__':
    do()
    #print(dateForFile())
    #print(dateForAnnotation())
    
