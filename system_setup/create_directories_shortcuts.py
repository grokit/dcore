#!/usr/bin/python3

"""
Generates shortcuts to folder that can be called from the shell.

On Windows, you can simply execute the 'cd' script, e.g:
    cdmusic

On Linux, you need to prepend '. ':
    . cdmusic

# TODO
- In windows/linux the directories shortcuts do not get cleaned-up
- Be able to add a directory map from anywhere: cdgen --add ., then query for name (or --name). This goes to a flat file that is referenced.
- @@a1: use a flat file instead of python file to store directories preferences. Allow to add a shortcut from command-line: "cdgen --add . dirtag"
    - this can also solve the "private data" issue: just have a flat file, implementation is all public, it will just complain of a missing key if not there.
"""

import dcore.system_description as sd

import os
import sys
import argparse

import private_data

_meta_shell_command = 'gendirs'

if __name__ == '__main__':
 
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--list', action = "store_true")
    parser.add_argument('-g', '--gen',  action = "store_true")

    args = parser.parse_args()
    
    dirsMap = sd.getDirsMap()
    
    if args.list == True:
        for k, v in dirsMap.items():
            print("%-15s: %s" % (k, v))
        sys.exit(0)
    elif args.gen == True: 
        file_ext, output_dir, file_template = sd.getPythonScriptsEnv()
        
        fileContentTemplate = sd.getAutogenFileTemplate()
        
        # Generate all folder shortcuts with 'cd' prefix.
        # So if a folder has the shortcut 'app', you can access it on the console by doing 'cdapp'
        for shortcut, folder in dirsMap.items():
            
            fileOut = dirsMap['dirs_shortcuts'] + "/" + 'cd' + shortcut + file_ext
            dswitch = ""
            if os.name == 'nt':
                dswitch = "/d "
            fileContent = fileContentTemplate.replace('__custom__', 'cd %s%s' % (dswitch, folder))
            
            fh = open(fileOut, 'w')
            fh.write(fileContent)
            fh.close()
            
            print('Created shortcut %s.' % fileOut)
            
            if os.name == 'posix':
                os.system('chmod +x %s' % fileOut)
    else:
        raise Exception("Invalid script arguments: %s." % args)
