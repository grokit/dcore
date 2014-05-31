#!/usr/bin/python3

"""
Generates shortcuts to folder that can be called from the shell.

On Windows, you can simply execute the 'cd' script, e.g:
    cdmusic

On Linux, you need to prepend '. ':
    . cdmusic
"""

import dcore.system_description as sd

import os

if __name__ == '__main__':
        
    dirsMap = sd.getDirsMap()
    
    file_ext, output_dir, file_template = sd.getPythonScriptsEnv()
    
    fileContentTemplate = sd.getAutogenFileTemplate()
    
    # Generate all folder shortcuts with 'cd' prefix.
    # So if a folder has the shortcut 'app', you can access it on the console by doing 'cdapp'
    for shortcut, folder in dirsMap.items():
        
        fileOut = output_dir + "/" + 'cd' + shortcut + file_ext
        fileContent = fileContentTemplate.replace('__custom__', 'cd %s' % folder)
        
        fh = open(fileOut, 'w')
        fh.write(fileContent)
        fh.close()
        
        print('Created shortcut %s.' % fileOut)
        
        if os.name == 'posix':
            os.system('chmod +x %s' % fileOut)
