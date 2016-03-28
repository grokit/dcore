"""
# USAGE

## Type a journal entry

    $ jl
    Here is my journal entry.
    !!!

Note that the '!!!' is a marker that you are done typing text.    
    
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
"""

_meta_shell_command = 'jl'

import os
import datetime
import argparse
import platform
import shutil

import dcore.data as data

stop = '!!!'

def dateForFile():
    return datetime.datetime.now().strftime("%Y-%m-%d")
    
def dateForFolder():
    return datetime.datetime.now().strftime("%Y-%m-%d")    
    
def dateForAnnotation():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
def getArgs():
    parser = argparse.ArgumentParser()
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
    inputBuf = ['# ' + dateForAnnotation() + '\n']
    fileContent = fh.read()
    fh = open(file, 'w')
    fh.write("\n".join(inputBuf).strip(stop) + '\n' + fileContent)

def appendContent(file, inputBuf):
    fh = open(file, 'r')
    fileContent = fh.read()
    fh = open(file, 'w')
    fh.write("\n".join(inputBuf).strip(stop) + '\n' + fileContent)
    
def getLatestScreenshotFilename():
    ## @@@@nix: proper path here (dcore?)
    screenshotFolder = r'C:\screenshots'
    
    files = [os.path.join(screenshotFolder, f) for f in os.listdir(screenshotFolder)]
    files.sort(key=lambda x: os.path.getmtime(x))
    return os.path.abspath(files[0])    
    
def do():    
    args = getArgs()
    
    if args.scratch:
        journalOutputPath = data.dcoreData()
        file = os.path.abspath(os.path.join(journalOutputPath, 'scratch.markdown'))
    else:
        journalOutputPath = os.path.abspath(os.path.join(data.dcoreData(), 'journals/%s/' % dateForFolder()))
        
        if not os.path.exists(journalOutputPath):
            print('No such path `%s`, creating.' % journalOutputPath)
            os.makedirs(journalOutputPath)
            
        file = os.path.abspath(os.path.join(journalOutputPath, '%s_journal.markdown' % dateForFile()))
    
    print('Using file: %s.' % file)
    if not os.path.isfile(file):
        #open(file, 'w').write('New file: %s.' % file)
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
            #c = 'vim %s' % file
            #c = 'gedit %s' % file
            c = 'kate %s' % file
        print(c)
        os.system(c)
        exit(0)
    
    print("Type '%s' to end." % stop)
    inputBuf = []
    while len(inputBuf) == 0 or inputBuf[-1].find(stop) == -1:
        try:
            lIn = input()
        except (EOFError):
            break        
        if lIn == None:
            break # reached EOF
        inputBuf.append( lIn )

    annotateDate(file)
    appendContent(file, inputBuf)
    
if __name__ == '__main__':
    do()
    #print(dateForFile())
    #print(dateForAnnotation())
    
