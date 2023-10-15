"""
# Find Files

Index all files under dir recursively and fast find.
fif -O <file> will open the file with default application if there is only 1 match.

# TODO

## As

- If -O +1 more than one match, ask which one to open.

## Bs

- Have an 'exact string' mode as an option.

- implement fif --fuid
        to me
        uid-abc
        uid-abc_tata
        marks file qith unique id
        warn on console if > 1 with same id on disk

- formalize data structure (could be just python freeze or flat 1 liner separated by commas)
- also store last mod as metadata
- also store hash (async, and can do 1MB at a time in files)
    - could / should use as a common library ("progressive hash")
- be able to tell when files are added, deleted, moved, etc -> leave a journal behind (I have an old script that does that, could revive it)

# BUGS

- It does not index and/or list files that begin with .period.
"""

import os
import argparse
import pickle
import datetime
import platform

import dcore.data as data
import dcore.utils as utils

_meta_shell_command = 'fif'

search_roots = [data.sync_root()]
cacheLoc = os.path.join(data.dcoreTempData(),
                        os.path.split(__file__)[1] + ".cache")

# Before automatically force regenerating.
cacheExpiryInSeconds = 7.0 * 24 * 60 * 60  

def get_args():
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
    args = get_args()

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

        for i, f in enumerate(F):
            print('(%.2i) %s' % (i, f))

        if args.open is True:
            open_ith = 0
            if len(F) > 1:
                open_ith = int(input('Open which one?\n'))

            ff = F[open_ith]
            utils.open_file_autoselect_app(ff)

if __name__ == '__main__':
    do()
