
import time
import datetime
import argparse

_meta_shell_command = 'times'

def getArgs():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args

   
if __name__ == '__main__':
    
    args = getArgs()
    
    print( "LocalTime:             %s." % datetime.datetime.now().isoformat(' ') )
    print( "UTCTime:               %s." % datetime.datetime.utcnow().isoformat(' ') )
    print( "UTC ahead of local by: %s." % str(datetime.datetime.utcnow() - datetime.datetime.now()) )
    
    
