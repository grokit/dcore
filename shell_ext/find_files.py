"""
# TODO

- Have an 'exact string' mode as an option.
"""

print('pre-Starting ff')

import os
import argparse
import pickle
import datetime
import platform

import dcore.data as data

_meta_shell_command = 'ff'

print('Starting ff')

search_roots = [r'~/sync']
if os.path.isdir('c:/src/working'):
    search_roots = ['c:/src/working', 'c:/david']
    #search_roots = ['c:/david/dev/books']

cacheLoc = os.path.join(data.dcoreTempData(), os.path.split(__file__)[1] + ".cache")
cacheExpiryInSeconds = 30*24*60*60

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--exact_match', action='store_true', default=False)
    parser.add_argument('grep', type=str, nargs='*', default = None)
    parser.add_argument('-r', '--reset', action="store_true", help="Force re-creation of the cache.")
    parser.add_argument('-o', '--open', action="store_true", help="Open in text editor all files that match.")
    args = parser.parse_args()
    return args

def getAllFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append(os.path.normpath(os.path.join(dirpath, f)))
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
    F = []

    for search_root in search_roots:
        search_root = os.path.expanduser(search_root)
        assert os.path.isdir(search_root)
        for f in getAllFiles(search_root):
            F.append(f)
    F = filterOutIfArrayInElement(F, ['node_modules', '.git',  '.hg', '__pycache__', r'Out\Functional'])
    return F

def do():
    args = getArgs()
    print(args)
    
    F = None
    if not args.reset and os.path.isfile(cacheLoc):
        print('Loading cache from: %s.' % cacheLoc)
        cache = pickle.load(open(cacheLoc, 'rb'))
        cacheAge = dateNow() - cache.date
        print('Cache age = %s.' % cacheAge)
        if cacheAge.total_seconds() < cacheExpiryInSeconds:
            F = cache.F
        else:
            print('Cache too old, wiping.')
            F = None
    
    if F is None:
        print("Generating cache from %s, this could take a while... grab a coffee and relax :)." % search_roots)
        F = gen()
        print('Saving cache at: %s.' % cacheLoc)
        pickle.dump(Cache(F), open(cacheLoc, 'wb'))
    
    if len(args.grep) != 0:
        gg = args.grep
        
        if args.exact_match == False:
            if type(gg) != list:
                gg = [gg]
            
            print('Filter-in with: %s.' % gg)
            for disc in gg:
                disc = disc.lower()
                F = filterInCaseInsensitive(F, disc)
        else:
            gg = " ".join(args.grep)
            gg = gg.lower()
            print('Filter-in with: %s.' % gg)
            F = filterInCaseInsensitive(F, gg)

        for f in F:
            print(f)
        
        if args.open is True:
            for f in F:
                if platform.system() == 'Windows':
                    cmd = 'np %s' % f
                else:
                    cmd = 'vim %s' % f
                os.system(cmd)

if __name__ == '__main__':
    do()
