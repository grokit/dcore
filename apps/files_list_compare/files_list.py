"""
# TODO 

- merge with files_list_compare

- auto save to home directory
    - ./Desktop/sdata/
    - ./Desktop/sdata/out/

- search function
"""

_meta_shell_command = 'files_index'

import json
import hashlib
import codecs
import os
import sys
import fnmatch
import time
import random
import argparse

def getAllFilesRecursively_DUPLICATE(in_allowedExtensionsGlobList, in_RootDir = '.'):
  """
  E.g.: getAllFilesRecursively(['*.txt'], './folder/to/files')
  E.g.: getAllFilesRecursively(['*.txt', '*.bat'])
  
  @note This function is ALWAYS recursive.
  @return List of fullpath string to files matching extensions provided.
  """
  
  #Allow user to call using both '*.txt' and ['*.txt']
  if( type(in_allowedExtensionsGlobList) == type('') ):
    in_allowedExtensionsGlobList = [in_allowedExtensionsGlobList]
  assert( type([]) == type(in_allowedExtensionsGlobList) )
  
  fileList = []
  for root, subFolders, files in os.walk(in_RootDir):
    for file in files: 
      
      add = False
      
      for glob in in_allowedExtensionsGlobList:
        if fnmatch.fnmatch(file, glob):
          add = True
      
      if add:
        fullPathFile = os.path.join(root, file)
        normalizedFullPath = os.path.abspath(fullPathFile)
        fileList.append(normalizedFullPath)
  
  return fileList

def getUniqueDateFile_DUP(base, ext = '.txt'):
    pre, post = os.path.split(base)
    filename = pre + '/' + time.strftime("%Y-%m-%d_") + post + ext
    
    while os.path.isfile(filename):
        filename = filename + '_'
    
    return filename

def getHash(filename):
    
    with open(filename, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def filterFile(file, nos):
    for no in nos:
        if file.find(no) != -1:
            return False
    return True
    
def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-o', '--output', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    
    assert sys.version_info.major >= 3
    args = getArgs()
    
    input_dir = '.'
    if args.input:
        input_dir = args.input
    output_dir = '.'
    if args.output:
        output_dir = args.output
    
    files = getAllFilesRecursively_DUPLICATE(['*'], input_dir)
    
    files = [file for file in files if filterFile(file, ['/.hg/', '/.git/', '__pycache__'])]

    fErrs = []
    fHash = []

    nFiles = len(files)
    cFile = 0
    nBound = 1000
    step = int(nFiles/nBound)
    if step == 0: step = 1
    boundaries = [i for i in range(0, nFiles, step)]
    
    for file in files:
        try:
            size = os.stat(file).st_size 
            
            hash = getHash(file)
            relpath = os.path.relpath(file)
            fullpath = os.path.abspath(file)
            
            # "relative_path": relpath
            fHash.append({"full_path": fullpath, "hash": hash, "size": size}) 
        except Exception as e:
            str = "%s, error: %s" % (file, e)
            #print(str)
            fErrs.append(str)
        
        cFile += 1
        if len(boundaries) != 0 and cFile > boundaries[0]:
            print( "%.2f%% done" % (100.0*(cFile/nFiles)) )
            boundaries = boundaries[1:]
    
    fn = getUniqueDateFile_DUP(output_dir + '/filesAndHash', '.txt')
    fnErrs = fn.replace('.txt', '_errs.txt')    
    
    if len(fErrs) > 0:
        fh = codecs.open(fnErrs, 'w', "utf-8")
        fh.write("\n".join(sorted(fErrs)))
        fh.close()
    
    fh = codecs.open(fn, 'w', "utf-8")
    
    #fHash.sort()
    for item in fHash:
        fh.write(json.dumps(item, sort_keys=True) + "\n")
    fh.close()
    
