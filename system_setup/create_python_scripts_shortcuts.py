#!/usr/bin/python3.4

"""
Search all python scripts for metadata indicating that a global shortcut for the shell system should be created.

# TODO

- cmdline args
    --> allow delete all shortcus based on magic number
"""

import os
import re
import sys

import dcore.search_files as fsearch
import dcore.system_description as sd

shell_meta_search = '_meta_shell_command'
_meta_shell_command = 'generate_shortcuts'

def findPyFiles():
    dirsMap = sd.getFilesAndFoldersMap()
    pyfiles = fsearch.getAllFilesRecursively('*.py', dirsMap['python_folder_public'])
    if dirsMap.get('python_folder_private') is not None:
        pyfiles += fsearch.getAllFilesRecursively('*.py', dirsMap['python_folder_private'])
    pyfiles = [pyfile for pyfile in pyfiles if pyfile.find('__') == -1]
    return pyfiles

def delCurrentShortcuts():
    
    file_ext, output_dir, file_template = sd.getPythonScriptsEnv()
    
    # @@b1: adapt for linux: scan all files where find magic number.
    shellFiles = fsearch.getAllFilesRecursively('*.bat', output_dir)
    
    toDel = []
    for file in shellFiles:
        fh = open(file, 'r')
        lines = fh.readlines()
        fh.close()
        
        for line in lines:
            if line.find(sd.magic_tag_intstr) != -1:
                toDel.append(file)
                break
    
    for file in toDel:
        print('Deleting: %s.' % file)
        os.remove(file)
    
def getMetadataFromPyFiles(pyfiles):
    """
    meta: (python file, shell command, special flags)
    """
    
    file_ext, output_dir, file_template = sd.getPythonScriptsEnv()
    
    meta = []
    
    for file in pyfiles:
        print('Processing file: %s.' % file)
        fh = open(file, 'r')
        lines = fh.readlines()
        fh.close()
        
        for line in lines:
            m = re.search(shell_meta_search + ".*=.*'(.*)'", line)
            if m is not None:
                # print('Found meta in file: ' + file)
                command = m.groups(0)[0]
                if len(command.split(' ')) > 1:
                    laucher = command.split(' ')[0]
                    args = " ".join(command.split(' ')[1:])
                else:
                    laucher = command
                    args = ''
                meta.append( (file, laucher, args) )
    
    return meta

def createShortcuts(lMeta):
    
    file_ext, output_dir, file_template = sd.getPythonScriptsEnv()
    dirsMap = sd.getFilesAndFoldersMap()
    
    for meta in lMeta:
        
        fileContent = file_template
        fileContent = fileContent.replace('__py_file__', meta[0])
        fileContent = fileContent.replace('__opt_cmd__', meta[2])
        
        fileOut = dirsMap['dirs_shortcuts'] + "/" + meta[1] + file_ext
        
        print( (meta, fileOut) )
        
        fh = open(fileOut, 'w')
        fh.write(fileContent)
        fh.close()
        
        if os.name == 'posix':
           os.system('chmod +x %s' % fileOut)    

def do():
    delCurrentShortcuts()
    pyFiles = findPyFiles()
    meta = getMetadataFromPyFiles(pyFiles)
    createShortcuts(meta)
    
if __name__ == "__main__":
	do()
