#!/usr/bin/python3.4

"""
Creates shell-accessible command line shortcuts for applications that have a meta-tag.

# TODO

- Merge with install.py?
"""

import os
import re
import sys

import dcore.search_files as fsearch
import dcore.data as data

shell_meta_search = '_meta_shell_command'
_meta_shell_command = 'generate_shortcuts'
magic_tag_intstr = 'GeneratedBy_%s_bg0sn9gtmq2jjper' % __file__

def isOK(file):
    if file.find('__'): return False
    dirname = os.path.dirname(file)
    if '/deprecated/' in dirname: return False
    return True

def findPyFiles():
    pyPublic = data.dcoreRoot()

    print('Getting files from: ' + pyPublic)

    pyfiles = fsearch.getAllFilesRecursively('*.py', pyPublic)
    pyfiles = [pyfile for pyfile in pyfiles if isOK(pyfile)]

    return pyfiles

def delCurrentShortcuts():
    raise Exception("Not implemented")

def getAutogenFileTemplate():

    magic_tag = 'Magic number for easy deletion: %s.' % magic_tag_intstr

    file_template = r"""
# Automatically created by '%s', do not modify.
# %s

__custom__ """ % (os.path.normpath(__file__), magic_tag)

    return file_template
    
def getMetadataFromPyFiles(pyfiles):
    """
    meta: (python file, shell command, special flags)

    :::meta[0, 1 or 2] is confusing. Just create a class with names entities.
    """
    
    meta = []
    for file in pyfiles:
        print('Processing file: %s.' % file)
        fh = open(file, 'r')
        lines = fh.readlines()
        fh.close()
        
        for line in lines:
            m = re.search(shell_meta_search + ".*=.*'(.*)'", line)
            if m is not None:
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
    
    file_template = getAutogenFileTemplate()
    placeForScriptsThatOSHasPATHSetTo = data.pathExt()
    
    for meta in lMeta:
        fileContent = file_template
        fileContent = fileContent.replace('__py_file__', meta[0])
        fileContent = fileContent.replace('__opt_cmd__', meta[2])

        fileContent = fileContent.replace('__custom__', 'python3 %s $*' % meta[0])
        
        fileOut = placeForScriptsThatOSHasPATHSetTo + "/" + meta[1] 
        fileOut = os.path.normpath(fileOut)
        
        print( (meta, fileOut) )
        
        fh = open(fileOut, 'w')
        fh.write(fileContent)
        fh.close()
        os.system('chmod +x %s' % fileOut)    

def do():
    pyFiles = findPyFiles()
    for p in pyFiles: print(p)
    if len(pyFiles) > 0:
        meta = getMetadataFromPyFiles(pyFiles)
        createShortcuts(meta)
    
if __name__ == "__main__":
	do()
