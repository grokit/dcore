
import os
import argparse
import pickle
import datetime

_meta_shell_command = 'ff'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('grep', type=str, nargs='?', default = None)
    # NOT CODED:
    #parser.add_argument('-f', '--filenames_only', action="store_true")
    args = parser.parse_args()
    return args

def getAllFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append( os.path.join(dirpath, f) )
    return F

def elementInList(f, filterArray):
    for e in filterArray:
        if e in f:
            return True
    return False

def filterOutIfArrayInElement(F, filterArray):
    return [f for f in F if not elementInList(f, filterArray)]

def filterInCaseInsensitive(F, astr):
    return [f for f in F if astr in f.lower()]

def dateNow():
    return datetime.datetime.now(datetime.timezone.utc)

def dateNowStr():
    return dateNow().isoformat()

class Cache:
    def __init__(self, F):
        self.F = F
        self.date = dateNow() 

def gen():
    # root = '~/sync/dev/Dropbox/scripts/dcore/shell_ext'
    root = '~/sync'
    F = getAllFiles(os.path.expanduser(root))
    F = filterOutIfArrayInElement(F, ['.git', '__pycache__'])
    return F

def do():
    args = getArgs()

    cache = None
    cacheLoc = os.path.expanduser('~/sync/ff_cache.pickle')

    F = None
    if os.path.isfile(cacheLoc):
        print('Loading cache from: %s.', cacheLoc)
        cache = pickle.load(open(cacheLoc, 'rb'))
        cacheAge = dateNow() - cache.date
        print('Cache age = %s.' % cacheAge)
        if cacheAge.total_seconds() < 12*(60*60):
            F = cache.F
        else:
            print('Cache too old, wiping.')

    if F is None:
        print('Generating cache... this could take a while... grab a coffee and relax :).')
        F = gen()
        print('Saving cache at: %s.' % cacheLoc)
        pickle.dump(Cache(F), open(cacheLoc, 'wb'))


    if args.grep is not None:
        args.grep = args.grep.lower()
        print('Filter-in with: %s.' % args.grep)
        F = filterInCaseInsensitive(F, args.grep)

    for f in F:
        print(f)

if __name__ == '__main__':
    do()
