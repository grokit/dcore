"""
# Find Files

Index all files under dir and fast find.
Thought about deleting this as I'm using less and less, but direct fif -o <file> is awesome for quick open of books and such.

# TODO

## As

- This is very good, especially if: -o -> open file, if > 1 offer open a list.
    BUT: non standard matching is counter intuitive. Just replace with regex.

## Bs

- Have an 'exact string' mode as an option.
- fif -o : open file for all indexed recursive(dirs), ask from list if > 1 match.

- implement fif --fuid
        to me
        uid-abc
        uid-abc_tata
        marks file qith unique id
        warn on console if > 1 with same id on disk

# BUGS

- It does not intex and list files that begin with .period.

- I should retire this for much simpler:
    - Store all fullpaths.
    - Search with regex.
"""

import os
import argparse
import pickle
import datetime
import platform

import dcore.data as data

_meta_shell_command = 'fif'

search_roots = [r'~/sync']
cacheLoc = os.path.join(data.dcoreTempData(),
                        os.path.split(__file__)[1] + ".cache")
cacheExpiryInSeconds = 0.5 * 24 * 60 * 60  # Before automatically force regenerating.


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('grep', type=str, nargs='*', default=None)
    parser.add_argument('-r',
                        '--reset',
                        action="store_true",
                        help="Force re-creation of the cache.")
    parser.add_argument('-O',
                        '--open',
                        action="store_true",
                        help="Open with OS-configured program.")
    parser.add_argument(
        '-e',
        '--vi',
        action="store_true",
        help="Open all files that match in (the BEST) text editor.")
    args = parser.parse_args()
    return args


def getAllFiles(rootdir='.'):
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
    astr = astr.lower()
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
    F = filterOutIfArrayInElement(
        F, ['node_modules', '.git', '.hg', '__pycache__', r'Out\Functional'])
    return F


def do():
    args = getArgs()

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
        print(
            "Generating cache from %s, this could take a while... grab a coffee and relax :)."
            % search_roots)
        F = gen()
        print('Saving cache at: %s.' % cacheLoc)
        pickle.dump(Cache(F), open(cacheLoc, 'wb'))

    if len(args.grep) != 0:
        gg = args.grep
        print('Filter-in with: [%s]. Ordering and case ignored.' %
              ", ".join(gg))
        for sub in gg:
            F = filterInCaseInsensitive(F, sub)

        for f in F:
            print(f)

        if args.open is True:
            assert len(F) == 1
            for f in F:
                cmd = 'xdg-open %s& >/dev/null 2>&1' % f
                print(cmd)
                os.system(cmd)

        if args.vi is True:
            for f in F:
                cmd = 'vi %s' % f
                os.system(cmd)


if __name__ == '__main__':
    do()
