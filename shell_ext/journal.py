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

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--open', action='store_true', default=False, help='Just opens the file in text editor.')
    parser.add_argument('-f', '--filename_copy_to_journal_directory', action='store_true', default=False, help='Copies the file to the journal current directory and inserts a link in the markdown file.')
    return parser.parse_args()
    
def date():
    return str(datetime.datetime.now()).split(' ')[0]

file = os.path.normpath(os.path.expanduser('~/dcore/journals/%s_journal.txt' % date()))
stop = '!!!'

if __name__ == '__main__':
    
    args = getArgs()
    
    print('Using file: %s.' % file)
    
    if args.filename_copy_to_journal_directory:
        raise Exception("Not implemented yet.")
    
    if args.open:
        if platform.system() == 'Windows':
            c = 'np %s' % file
        else:
            c = 'vim %s' % file
        print(c)
        os.system(c)
        exit(0)
    
    if not os.path.isfile(file):
        open(file, 'w').write('New file for %s.' % date())
    
    fh = open(file, 'r')
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
    
    inputBuf = ['# ' + date() + '\n'] + inputBuf
    
    fileContent = fh.read()
    fh = open(file, 'w')
    fh.write("\n".join(inputBuf).strip(stop) + '\n' + fileContent)
