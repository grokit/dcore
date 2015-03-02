
"""
Analyze plaintext log files, reorganizes by section based on the opening and closing tags.

# TODO

- Warn if an 'open marker' is found when still looking for a 'closed marker'.
- Ignore capitalization while sorting
- This is wayyyy too OO, clean-up!

# BUGS

"""

_meta_shell_command = 'logsa'

import argparse
import string
import os
import sys

def getArgs():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('file', type = str, default = None)
    parser.add_argument('-w', '--write_back', default = None, action = "store_true", help = "true: automatically overwrite the source file with the results.")

    parser.add_argument('-s', '--sections_only', default = None, action = "store_true", help = "Only prints section names and location.")
    args = parser.parse_args()
    
    return args

def to_ascii_or_underbar(bytes):
  
  str = []
  
  for byte in bytes:
    #10: \n, 13: \r
    if (ord(byte) >= 32 and ord(byte) <= 126) or ord(byte) == 10 or ord(byte) == 13:
      str.append(byte)
    else:
      str.append('_')
   
  return "".join(str)  
    
class Section:
  "One individual section"
  
  def __init__(self):
    self.__title = 'NONE'
    self.__linesStartFinish = (-1,-1) #(start,finish)
    self.__content = 'NO CONTENT'
  
  def set(self, title, content, lines):

    if title == '':
      raise Exception( 'Empty caption at line ' + str(lines[0]) )
      
    self.__title = title
    
    assert( len(lines) == 2 )
    assert( lines[0] < lines[1] )
    
    self.__linesStartFinish = lines
    self.__content = content
    
  def get(self):
    return (self.__title, self.__linesStartFinish, self.__content)
  
  def getTitle(self):
    return self.__title
  
  def getLinesStartFinish(self):
    return self.__linesStartFinish
  
  def getContent(self):
    return self.__content
  
  def __lt__(self, other):
    return self.__title < other.__title
  
  def __repr__(self):
    return self.__title
    
  
class Sections:
  "Sections read form the file."
  
  def __init__(self, sectionReader):
    self.__sections = sectionReader.read()
  
  def sortSections(self):
    try:
      self.__sections.sort()
    except TypeError:
      for section in self.__sections:
        print(section)
      raise
  
  def getSections(self):
    return self.__sections
  
  def getTitlesInfo(self):
    
    #TLC = (title, lines, content)
    TLC = []    
    for section in self.__sections:
      TLC.append( section.get() )
    
    titlesInfo = []
    for section in TLC:
      numC = section[1][0]
      titlesInfo.append( "%.4i: %s\n" % (numC, section[0]) )
    
    return "".join(titlesInfo)

class MarkupConvention:
  markingOpen = '#~'
  markingClose = '~#'
  
  homelessMarkup = '__MARKUP__NO_SECTION_TEXT__MARKUP__'

class SectionWriter:
  
  def __init__(self, sections):
    sections.sortSections()
    self.__sections = sections
  
  def generate(self):
      
    lstSection = self.__sections.getSections()
    
    #Find HomelessSection, remove from group and add first
    homelessSection = None
    for section in lstSection:
      if section.getTitle() == MarkupConvention.homelessMarkup:
        assert homelessSection == None
        homelessSection = section
        lstSection.remove(section)
    
    #If found, append homeless text first in output
    str_AllSections = []
    if homelessSection is not None:
      str_AllSections += homelessSection.getContent()
    
    for section in lstSection:
      title = section.getTitle()
      lines = section.getLinesStartFinish()
      content = section.getContent()
      
      str_AllSections.append( MarkupConvention.markingOpen )
      str_AllSections.append( section.getTitle() + ':\n' )
      str_AllSections.append( section.getContent() )
      str_AllSections.append( MarkupConvention.markingClose + '\n\n' )
    
    return "".join(str_AllSections)
    
  def write(self, filename):
    
    str_AllSections = self.generate()
    
    fh = open(filename, 'wb')
    fh.write(str_AllSections.encode('utf-8'))
    fh.close()

class SectionReader:
  
  def __init__(self, filename):
    
    "RAW sections including markings"
    self.__sections = []
    self.__textOutsideSections = ''
    
    fh = open(filename, 'r', encoding='utf-8')
    fileLines = fh.readlines()
    fh.close()
    
    #Detach the sections from the text's body
    self.__buildSections(fileLines)
  
  def read(self):
    return self.__sections
  
  def __buildSections(self, fileLines):
    
    currSection = Section()
    buffer = []
    
    lineStart = -1
    buffering = False
    header = ''
    lineEnd = -1
    
    lineCount=0
    for line in fileLines:
      lineCount = lineCount + 1
      
      if line.find(MarkupConvention.markingOpen) != -1:
        buffering = True
        lineStart = lineCount
        buffer.append( line )
        
      elif line.find(MarkupConvention.markingClose) != -1:
        buffering = False
        
        #Build section
        lineEnd = lineCount
        
        assert buffer[0].find(MarkupConvention.markingOpen) != -1
        title = buffer[0].strip().strip(MarkupConvention.markingOpen).strip().strip(':')
        buffer = "".join(buffer[1:])
        
        #Build the section item
        currSection.set(title, buffer, (lineStart, lineEnd))
        self.__sections.append( currSection )
        currSection = Section()
        
        #Clear buffers
        buffer = []
        line = ''
      
      elif buffering:
        buffer.append( line )
      else:
        if line != '':
          self.__textOutsideSections += line
    
    #Write the special section for text not belonging in a section:
    homelessSection = Section()
    homelessSection.set(MarkupConvention.homelessMarkup, self.__textOutsideSections, (0,999)) #@tag: Do not know what to do with that
    self.__sections.append( homelessSection )

if __name__ == "__main__":
  
  args = getArgs()
  print(args)
  
  filename = args.file
  
  sections_read = SectionReader( filename )
  sections_info = Sections( sections_read )
  
  if args.sections_only:
      print ( to_ascii_or_underbar( sections_info.getTitlesInfo() ) )
      sys.exit(0)
  
  sections_writer = SectionWriter( sections_info )
  
  if not args.write_back:
      print( sections_writer.generate() )
      sys.exit(0)
  
  sections_writer.write(filename)
