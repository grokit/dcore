"""
# Overview 

Take notes from command-line, put them in note-taking system.

It removes hurdles that hinders quick note-taking:

    - Native to console, avoid having to switch to a UI application and works on all OS.
    - Fully scriptable.
    - Centralizes all notes to a folder, avoid having to `pushd.; cd ~/notes; take notes; popd;` everytime you want to take a note.
    - Append some metadata such as time of entry to notes.
    - Have convention for entering notes that make them easily searcheable by title or tags.

## Type a journal entry

    $ nn
    Here is my journal entry.
    :end

Note that the ':end' is a marker that you are done typing text. Until it is typed, the notes is not written to HD.
    
## Insert file as journal entry (directly in text file)
    
    $ nn < file

## Save a copy of file in same directory as journal
    
    $ nn -f filename
    
"""

_meta_shell_command = 'nn'

import os
import datetime
import argparse
import platform
import shutil

stop = ':end'

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
    parser.add_argument('-e', '--edit', action='store_true', default=False, help='Open target file (current note or scratch) in text editor.')
    parser.add_argument('-x', '--explore_folder', action='store_true', default=False, help='Open journal folder in nautilus / explorer.')
    parser.add_argument('-f', '--filename_copy_to_journal_directory', help='Copies the file to the journal current directory and inserts a link in the markdown file.')
    parser.add_argument('-p', '--save_screenshot_to_current_journal', action='store_true', default=False, help="Copies latest file in screenshot directory and copies to folder which contains today's journal.")
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
    inputBuf = ['(time::' + dateForAnnotation() + ')\n']
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
    dataLocation = os.path.expanduser('~/sync/notes')
    try:
        # If you are using dcore system, take root from there.
        import dcore.data as data
        dataLocation = data.dcoreData()
    except ImportError as e:
        pass

    print('Using folder: %s.' % dataLocation)
    if not os.path.isdir(dataLocation):
        print('Folder does not exist, creating.')
        os.makedirs(dataLocation)

    args = getArgs()
    
    journalOutputPath = dataLocation
    file = os.path.abspath(os.path.join(os.path.join(journalOutputPath, ''), 'ingest.md'))
    
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
        
    if args.edit:
        annotateDate(file)
        if platform.system() == 'Windows':
            c = 'np %s' % file
        else:
            c = 'vim %s' % file
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
