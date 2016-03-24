"""
# Documentation

`dr -r` will permanently remember current directory.
`dr` lists all directory remembered and their tags.

Each directory gets a tag (by default 00...99), to go to that directory simply type:
. cd<tag>

e.g:
cd01
cd03

Note that in Windows you do not need the `. ` prefix, simply type cd01, cd02.

# TODO
# BUGS
"""

_meta_shell_command = 'dr'


import sys
import os
import argparse
import platform

try:
    from tkinter import Tk
except:
    pass

import dcore.data as data
    
path_ext_folder = data.pathExt()
cacheFile = os.path.join(data.dcoreData(), '%s.cache' % os.path.split(__file__)[1])
cacheFilePerimated = cacheFile + ".deleted"
tempBatch = cacheFile + '.temp.bat'

def rememberDirs():
    dirs = [os.getcwd()]
    
    dirs += getFileContent()

    bad = [d for d in dirs if not os.path.isdir(d) and not (len(d.split(',')) == 2 and os.path.isdir(d.split(',')[1]))]
    print('Removing non-existent directories: %s.' % bad)
    dirs = [d for d in dirs if d not in bad]
    
    setFileContent( dirs )
    
    # need to read again because might be different if there are duplicates
    dirs = getFileContent()
    
    # create shortcut files
    if os.path.isdir(path_ext_folder):
        i = 0
        for dir in dirs:
            
            shortcut = ''
            if ',' in dir: 
                shortcut, dir = dir.split(',')
            
            new_file = os.path.join(path_ext_folder, r'cd%02d' % i)
            if platform.system() == 'Windows':
                new_file += '.bat'
            fh = open(new_file, 'w')
            if platform.system() == 'Windows':
                fh.write('cd /d "%s"' % dir)
            else:
                fh.write('cd "%s"' % dir)
            
            if shortcut != '':
                new_file = os.path.join(path_ext_folder, r'cd%s' % shortcut)
                if platform.system() == 'Windows':
                    new_file += '.bat'
                fh = open(new_file, 'w')
                if platform.system() == 'Windows':
                    fh.write('cd /d "%s"' % dir)
                else:
                    fh.write('cd "%s"' % dir)
            
            fh.close()
            i += 1
    else:
        raise Exception(path_ext_folder)
        
def getFileContent():
    """
    # File Format
    
        [tag,]<file>
        ...
        [tag,]<file>
    
    e.g:
    
        jl,/journal
        /etc
    
    '/etc' is a non-tag shortcut, will be accessible with a number.
    '/journal' will be accessible with a number OR cdjl.
    """
    
    fh = open(cacheFile, 'r')
    data = fh.read()
    fh.close()
    
    data = data.splitlines()
    
    return data
    
def setFileContent(fileList):
    # Eliminate duplicates.
    fileList = list(set(fileList))
    fileList.sort()
    
    fh = open(cacheFile, 'w')
    
    for file in fileList:
        fh.write(file)
        fh.write("\n")        
    fh.close()
    
def printStoredDirs():
    data = getFileContent()
    
    i = 0
    for file in data:
        print("%02d: %s" % (i, file))
        i += 1
    
def clearDirs():
    fh = open(cacheFilePerimated, 'a')
    for file in getFileContent():
        fh.write( file )
        fh.write( "\n" )
    fh.close()
    
    os.remove(cacheFile) 
    
def do():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-r', '--remember', action="store_true")
    parser.add_argument('-p', '--print', action="store_true")
    parser.add_argument('-c', '--clear', action="store_true")
    parser.add_argument('-e', '--edit', action="store_true")
    parser.add_argument('-g', '--goto_clip', type=int)
    
    args = parser.parse_args()
    #print(args)
    print('Using cache file: %s.' % cacheFile)
    
    if not os.path.isfile(cacheFile):
        fh = open(cacheFile, 'w')
        fh.write('')
        fh.close()
    
    if args.print:
        printStoredDirs()
        exit(0) 
    
    if args.clear:
        clearDirs()
        exit(0) 
    
    if args.edit:
        if platform.system().lower() == 'windows':
            os.system('np ' + cacheFile)
        else:
            os.system('vim ' + cacheFile)
        exit(0)      
    
    if args.remember:
        rememberDirs()
        printStoredDirs()
        exit(0)        
    
    if args.goto_clip != None:
        filec = getFileContent()
        dir = filec[args.goto_clip]
        
        if Tk is not None:
            r = Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(dir)
            r.destroy()  
        else:
            print('Tk not available, clipboard functions will not work.')
        
        print("'%s' now in clipboard" % dir)
        exit(0)       
    
    printStoredDirs()
    
if __name__ == '__main__':
    do()
        
