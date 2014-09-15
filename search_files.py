
import os
import fnmatch

def getAllFilesRecursively(in_allowedExtensionsGlobList, in_RootDir = '.'):
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
      
      #@tag TODO: re-use filterFilesByExtension here
      for glob in in_allowedExtensionsGlobList:
        if fnmatch.fnmatch(file, glob):
          add = True
      
      if add:
        fullPathFile = os.path.join(root, file)
        normalizedFullPath = os.path.abspath(fullPathFile)
        fileList.append(normalizedFullPath)
  
  return fileList

def filterFilesByExtension(lstFullPathFilenames, lstExtensionsToKeep):
  
  fileList = []
  for file in lstFullPathFilenames:
    add = False
    for glob in lstExtensionsToKeep:
      if fnmatch.fnmatch(os.path.split(file)[1], glob):
        add = True
    if add:
      fileList.append(file)
  return fileList

def getAllFoldersRecursively(in_RootDir = '.'):
  """
  @tag: BETA
  """
  
  folderList = []
  for root, subFolders, files in os.walk(in_RootDir):
    for folder in subFolders:
      folder_fullpath = os.path.join(root, folder)
      assert os.path.isdir(folder_fullpath)
      folderList.append(folder_fullpath)
  return folderList

def test_module():
  #Just run
  folders = getAllFoldersRecursively()
  #assert os.path.dirname(__file__) in folders
  
  #Simple check
  files = getAllFilesRecursively(['*.py'], '.')
  #assert os.path.split(__file__)[1] in files  #not ness run from curr.path!
  
  myFiles = ['c:\\folder1\\aFile.cpp', 
             'c:\\folder2\\bFile.cpp', 
             'c:\\folder3\\cFile.exe', 
             'c:\\folder4\\app_launch.bin',
             'c:\\folder4\\bin_but_not_ext.exe',
             'c:\\folder4\\Makefile'
             ]
  myFilesFiltered = filterFilesByExtension(myFiles, ['*.cpp', '*.bin', 'Makefile'])
  print (myFilesFiltered)
  assert myFiles[0] in myFilesFiltered
  assert myFiles[1] in myFilesFiltered
  assert myFiles[2] not in myFilesFiltered
  assert myFiles[3] in myFilesFiltered
  assert myFiles[4] not in myFilesFiltered
  assert myFiles[5] in myFilesFiltered

if __name__ == '__main__':
  test_module()
