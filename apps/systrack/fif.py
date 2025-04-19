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
import sqlite3
import time

import dcore.data as data
import dcore.utils as utils

_meta_shell_command = 'fif'

_SEARCH_ROOT_FOLDERS = [ os.path.expanduser(ff) for ff in [ data.sync_root(), '~/low_sync', '~/crmounts/lowsync_media']]
_CACHE_FILE_LOCATION = os.path.join(data.dcoreTempData(),
                                    os.path.split(__file__)[1] + ".cache")
_SQL_DB_FILENAME = os.path.join(data.dcoreTempData(), "fif_file_index.db")

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


def list_all_files():
    F = []

    for search_root in _SEARCH_ROOT_FOLDERS:
        search_root = os.path.expanduser(search_root)
        assert os.path.isdir(search_root)
        for f in getAllFiles(search_root):
            f = os.path.abspath(os.path.join(search_root, f))
            if not os.path.islink(f):
                F.append(f)
    F = filterOutIfArrayInElement(
        F, ['node_modules', '.git', '.hg', '__pycache__', r'Out\Functional'])
    return F


def do_sql_dump_and_compate(filenames):
    """
    New/experimental: dump to SQL database to make it possible to track files added, deleted & spot accidental deleted of uid-files.
    """
    print(f'Saving to {_SQL_DB_FILENAME}')
    conn = sqlite3.connect(_SQL_DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fif_file_index (
        filepath TEXT,
        last_mod_unix_s INTEGER,
        last_crawled_unix_s INTEGER,
        PRIMARY KEY (filepath)
    )
    ''')
    now_unix_s = int(time.time() * 1)
    for filename in filenames:
        filename_last_mod_unix_s = os.path.getmtime(filename)
        cmd = '''INSERT OR REPLACE INTO fif_file_index (filepath, last_mod_unix_s, last_crawled_unix_s) VALUES (?, ?, ?)'''
        args = (filename, filename_last_mod_unix_s, now_unix_s)
        #print(cmd, args)
        cursor.execute(cmd, args)
    conn.commit()
    conn.close()


def do():
    args = get_args()

    F = None
    if not args.reset and os.path.isfile(_CACHE_FILE_LOCATION):
        print('Loading cache from: %s.' % _CACHE_FILE_LOCATION)
        cache = pickle.load(open(_CACHE_FILE_LOCATION, 'rb'))
        cacheAge = dateNow() - cache.date
        print('Cache age = %s.' % cacheAge)
        if cacheAge.total_seconds() < cacheExpiryInSeconds:
            F = cache.F
        else:
            print('Cache too old, wiping.')
            F = None

    if F is None:
        print(
            "Generating cache from %s, this could take a while... have a tea and relax :)." %
            _SEARCH_ROOT_FOLDERS)
        F = list_all_files()
        print(f'Saving cache at: {_CACHE_FILE_LOCATION}')
        pickle.dump(Cache(F), open(_CACHE_FILE_LOCATION, 'wb'))
        do_sql_dump_and_compate(F)

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
