r"""
TODO

#A

- have an actual n-gram index mode so that can avoid searching in some files for keyword set

#B

- more thoughtful solution for lowercasing
- allow to search a subset of extensions
- be able to say which file extentions are included in DB

#C
"""

_meta_shell_command = 'scode'

## local imports
import options
import db

## std imports
import os
import argparse
import sqlite3
import timeit

# @@maybe move all of that to config
DB_SUBFOLDER = '.code_search_cache'
DB_FILENAME = 'db.db'

def getArgs():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('search_string', nargs = '*', default="", type=str)
    
    parser.add_argument('-d', '--dir_of_db', default = None)
    parser.add_argument('-c', '--build_cache', action = "store_true")
    parser.add_argument('-v', '--verbose', type = int)
    parser.add_argument('-f', '--search_filename', action = "store_true")
    parser.add_argument('-p', '--search_filename_path', action = "store_true")
    parser.add_argument('-r', '--regex', action = "store_true")
    parser.add_argument('-t', '--time_profile', action = "store_true")
    parser.add_argument('-e', '--extension_filter', type = str, default = None, help="@@IN CONSTRUCTION -- Only search in filenames with the extensions provided. E.g: -f .cpp .hpp .py")
    
    args = parser.parse_args()
    
    return args

def findRepositoryByBackTracking():
    """
    If not found, pick current dir.
    """
    
    cLookBack = '.'
    while(True):
        cDir = os.path.abspath(cLookBack)
        print("Searching in %s" % cDir)
        if os.path.isdir( os.path.join(cDir, DB_SUBFOLDER) ):
            return cDir
        else:
            if os.path.abspath(cLookBack) == os.path.abspath(cLookBack + '/..'):
                return os.path.abspath('.')
            cLookBack = cLookBack + '/..'
    
    return cDir

def mainPlusTime():
    
    simple = False
    
    if simple:
        timeit_res = timeit.timeit( 'main()', number = 1 )
        print("Time: %s" % timeit_res)
    else:
        import cProfile    
        cProfile.run('main()')

def filterExtStrToArray(filterExt):
    """
    ".txt .html" => [".txt", ".html"]
    """
    
    if filterExt is None:
        return []
    
    fe = filterExt.split(" ")
    
    for f in fe:
        assert f[0] == "."
    
    return fe
        
def main():
    
    args = getArgs()
    print(args)
    
    if args.dir_of_db is None:
        args.dir_of_db = findRepositoryByBackTracking()
        print("Using repository in: %s" % args.dir_of_db)
    
    db_fullpath = os.path.join(args.dir_of_db, DB_SUBFOLDER, DB_FILENAME)
    
    (db_folder, throwaway) = os.path.split(db_fullpath)
    
    if args.build_cache == True or not os.path.isdir(db_folder):
        db.reset(db_folder)
        db.createAndIndex(db_fullpath, args.dir_of_db)
        
        if args.build_cache == True:
            exit(0)
    
    strToSearch = " ".join(args.search_string)
    #strToSearch = args.search_string
    
    if args.search_filename:
        db.searchFilename(db_fullpath, strToSearch, args.regex)
        exit(0)
    
    if args.search_filename_path:
        db.searchFilenamePath(db_fullpath, strToSearch, args.regex)
        exit(0)
        
    db.search(db_fullpath, strToSearch, filterExtStrToArray(args.extension_filter), args.regex)
    
if __name__ == '__main__':
    
    args = getArgs()
    
    if not args.time_profile:
        main()
    else:
        mainPlusTime()
