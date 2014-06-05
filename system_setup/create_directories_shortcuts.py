#!/usr/bin/python3

"""
Generates shortcuts to folder that can be called from the shell.

On Windows, you can simply execute the 'cd' script, e.g:
    cdmusic

On Linux, you need to prepend '. ':
    . cdmusic

# TODO
- In windows/linux the directories shortcuts do not get cleaned-up
- @@a1: relies of 'path_ext' of current directory being on path for windows. Find a better way (auto add to path, use system-mandated-directory e.g: %appdata%).
"""

import dcore.system_description as sd

import os
import sys
import argparse

import private_data

_meta_shell_command = 'cdgen'

if __name__ == '__main__':
 
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--list', action = "store_true")
    parser.add_argument('-g', '--gen',  action = "store_true")

    args = parser.parse_args()
        
    dirsMapPublic = sd.getDirsMap()
    dirsMapPrivate = {}
    try:
        dirsMapPrivate = private_data.getDirsMapPrivate()
    except Exception as e:
        print("%s cannot get private directories: %s." % (__file__, e))
    dirsMap = dict(list(dirsMapPublic.items()) + list(dirsMapPrivate.items()))
    
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
            
            fileOut = output_dir + "/" + 'cd' + shortcut + file_ext
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
