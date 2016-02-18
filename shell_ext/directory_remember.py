"""
# TODO

- automatically create 'cd1.bat, cd2.bat, ...' OR for -g, create a temp bat file and execute
- dr -r, cd00 <-- goes to latest added

# TODO-B

- rdir . tata --> create .bat file so that cdtata will access this directory.

- global file to specify computer-specific dirs

- when adding a new cd<X>, do it at the end, not begin (avoid moving cd<x> for no reason)

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

    bad = [d for d in dirs if not os.path.isdir(d)]
    print('Removing non-existent directories: %s.' % bad)
    dirs = [d for d in dirs if os.path.isdir(d)]
    
    setFileContent( dirs )
    
    # need to read again because might be different if there are duplicates
    dirs = getFileContent()
    
    # create shortcut files
    if os.path.isdir(path_ext_folder):
        i = 0
        for dir in dirs:
            new_file = os.path.join(path_ext_folder, r'cd%02d.bat' % i)
            fh = open(new_file, 'w')
            fh.write('cd /d "%s"' % dir)
            fh.close()
            i += 1
    else:
        raise Exception(path_ext_folder)
        
def getFileContent():
    fh = open(cacheFile, 'r')
    data = fh.read()
    fh.close()
    
    data = data.splitlines()
    
    return data
    
def setFileContent(fileList):
    
    fh = open(cacheFile, 'w')
    
    fileList = list(set(fileList))
    fileList.sort()
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
        
