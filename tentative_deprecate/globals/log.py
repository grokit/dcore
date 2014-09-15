
import sys
import time

from . import resources

class LogLevel:
    Trace = 0
    Info = 1
    Debug = 2
    Warning = 3
    Error = 4
    
    def nameFromInt(i):
        
        d = {
            0 : 'Trace',
            1 : 'Info',
            2 : 'Debug',
            3 : 'Warning',
            4 : 'Error'}
        
        return d[i]
        
def error(logStr, silence = False):
    __log(LogLevel.Error, logStr, silence)
    
def warning(logStr, silence = False):
    __log(LogLevel.Warning, logStr, silence)
    
def debug(logStr, silence = False):
    __log(LogLevel.Debug, logStr, silence)
    
def info(logStr, silence = False):
    __log(LogLevel.Info, logStr, silence)

def trace(logStr, silence = False):
    __log(LogLevel.Trace, logStr, silence)
    
def __log(logLevel, logStr, silence = False):
  strGlobalLogFilename = resources.getFileFromTag('GlobalLogFile', False)
  
  llStr = str(LogLevel.nameFromInt(logLevel))
  
  fh = open ( strGlobalLogFilename, 'a' )
  fh.write (llStr + ", " +  __getLogTime() + ": " + logStr + '\n' )
  fh.close() 
  
  if not silence:
    print(logStr)

def __getLogTime():
  return time.strftime("%Y-%m-%d %H:%M:%S")

def test_module():
  log("log's module test log entry")
  
if __name__ == '__main__':
  test_module()