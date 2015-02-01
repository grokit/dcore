"""
_meta_shell_command = 'dr'

# TODO

- rdir . tata --> create .bat file so that cdtata will access this directory.

# TODO-B

- automatically create 'cd1.bat, cd2.bat, ...' OR for -g, create a temp bat file and execute

- global file to specify computer-specific dirs

- when adding a new cd<X>, do it at the end, not begin (avoid moving cd<x> for no reason)

# BUGS

- cd<X> are messed-up (wrong number, offset of 1)

"""

import sys
import os
import argparse

from tkinter import Tk

cacheFile = r't:\temp\%s.cache' % os.path.split(__file__)[1]
cacheFilePerimated = cacheFile + ".deleted"
tempBatch = cacheFile + '.temp.bat'

path_ext_folder = os.path.join(os.environ['DTG_ROOT'], r'scripts-private\path_ext')

def remember_dir():
    
    dirs = [os.getcwd()]
    
    dirs += get_file_content()
    
    set_file_content( dirs )
    
    # need to read again because might be different if there are duplicates
    dirs = get_file_content()
    
    # create shortcut files
    i = 0
    for dir in dirs:
        new_file = path_ext_folder + r'\cd%s.bat' % i
        fh = open(new_file, 'w')
        fh.write('cd "%s"' % dir)
        fh.close()
        i += 1

def get_file_content():
    fh = open(cacheFile, 'r')
    data = fh.read()
    fh.close()
    
    data = data.splitlines()
    
    return data
    
def set_file_content(fileList):
    
    fh = open(cacheFile, 'w')
    
    file_cache = {}
    for file in fileList:
        if file_cache.get(file) == None:
            file_cache[file] = True
            fh.write(file)
            fh.write("\n")        
    fh.close()
    
def print_stored_dirs():
    data = get_file_content()
    
    i = 0
    for file in data:
        print("%02d: %s" % (i, file))
        i += 1
    
def clear_dirs():
    fh = open(cacheFilePerimated, 'a')
    for file in get_file_content():
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
        print_stored_dirs()
        exit(0) 
    
    if args.clear:
        clear_dirs()
        exit(0) 
    
    if args.edit:
        os.system('np ' + cacheFile)
        exit(0)      
    
    if args.remember:
        remember_dir()
        print_stored_dirs()
        exit(0)        
    
    if args.goto_clip != None:
        filec = get_file_content()
        dir = filec[args.goto_clip]
        
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(dir)
        r.destroy()  
        
        print("'%s' now in clipboard" % dir)
        exit(0)       
    
    print_stored_dirs()
    
if __name__ == '__main__':
    do()
        