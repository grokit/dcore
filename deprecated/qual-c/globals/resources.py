"""
Contains functions that returns information that the user might need across all modules.

It is meant to be easy to customize and allows some tests (for example to list all the 
directories available and check for their existence).
"""

import os

class __Global_Data:
  __PRIVATE_TEMPLATE_SCRIPTS_TEST_DIR_ROOT = 'C:/David/scripts/tests'
  
  __Tag_to_Dir = {
  'LogsOutputDir' : r'C:\david\sync\Dropbox\scripts\logs_output_dir'
  }
  
  __Tag_to_File = {
  'GlobalLogFile' : __Tag_to_Dir['LogsOutputDir'] + '/GlobalScriptsLogs.txt'
  }  
  
  def __init__(self):
    for dir in self.__Tag_to_Dir.values():
      if not os.path.isdir(dir):
        raise Globals_Error("Invalid global path: {1} ({0}).".format(__file__, dir))
    for file in self.__Tag_to_File.values():
      if not os.path.isfile(file):
        raise Globals_Error("Invalid global file: {1} ({0}).".format(__file__, file))
  
  def Get_TagToDir(self):
    return self.__Tag_to_Dir

  def Get_TagToFile(self):
    return self.__Tag_to_File
  
#On error
class Globals_Error(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

##
## Public Exported Functions
##

def getDirFromTag( tag ):
  """
  Match a tag with the directory dictionary;
  If the tag does no exists or the directory is not valid it raises a 'Globals_Error'.
  """
  
  global_Data = __Global_Data()
  
  if not tag in global_Data.Get_TagToDir().keys():
    raise Globals_Error("Tag: '" + tag + "' not found")
  
  path = global_Data.Get_TagToDir()[tag]
  
  if not os.path.exists(path):
    raise Globals_Error("Path not found: " + path)
  
  return path

def getFileFromTag( tag, forceExist = True ):
  """
  Match a tag with the file dictionary;
  If the tag does no exists or the directory is not valid it raises a 'Globals_Error'.
  """
  
  global_Data = __Global_Data()
  
  if not tag in global_Data.Get_TagToFile().keys():
    raise Globals_Error("Tag: '" + tag + "' not found")
  
  file = global_Data.Get_TagToFile()[tag]
  
  if not os.path.exists(file) and forceExist:
    raise Globals_Error("File not found: " + path)
  
  return file

def test_module():
  globalData = __Global_Data()
  
if __name__ == '__main__':
  test_module()
