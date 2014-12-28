
import time
import datetime
import calendar
import argparse

_meta_shell_command = 'times'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("time_to_convert", nargs='?', default=None, help="Expects format: Thu, 04 Dec 2014 22:06:29 GMT.")
    args = parser.parse_args()
    return args

def toGLFormat(ttime):
    return ttime.strftime(format("%Y%m%d_%H%M%S%f"))

def toAllPrint(ttime):
    #print(type(ttime))
    #print(ttime)
    return toGLFormat(ttime) + " / " + ttime.isoformat(' ')

if __name__ == '__main__':
    
    args = getArgs()
    
    if args.time_to_convert is None:
        print( "LocalTime:             %s." % toAllPrint(datetime.datetime.now()) )
        print( "UTCTime:               %s." % toAllPrint(datetime.datetime.utcnow()) )
    else:
        ttime  = time.strptime(args.time_to_convert, "%a, %d %b %Y %H:%M:%S %Z")
        ttime = datetime.datetime.utcfromtimestamp(calendar.timegm((ttime)))
        print( "Time       :               %s." % toAllPrint(ttime) )
        localDelta = datetime.datetime.now() - datetime.datetime.utcnow()
        print( "Time local :               %s." % toAllPrint(ttime + localDelta) )

    print( "UTC ahead of local by: %s." % str(datetime.datetime.utcnow() - datetime.datetime.now()) )
    
    
