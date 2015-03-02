"""
@@BUG:

- Simple search is case sensitive unless I lower everything at scraping time. (see: @@lowercase_bug)

See: 
    SQL-centric: http://www.sqlite.org/docs.html
    Python-centric: https://pysqlite.readthedocs.org/en/latest/sqlite3.html
        - Regex: http://stackoverflow.com/questions/5365451/problem-with-regexp-python-and-sqlite
"""

import options
import decorate

import dcore.search_files

import os
import re
import shutil
import fnmatch
import sqlite3
import codecs

def reset(path):
    print("db.reset (%s)" % path)
    
    if os.path.isdir(path):
        shutil.rmtree(path)

def createAndIndex(db_file_fullpath, root_dir_to_index):
    print("db.createAndIndex %s, %s" % (db_file_fullpath, root_dir_to_index))
    
    (db_dir, db_file) = os.path.split(db_file_fullpath)
    
    if not os.path.isdir(db_dir):
        os.makedirs(db_dir)
    
    # connect
    conn = sqlite3.connect(db_file_fullpath)
    c = conn.cursor()
    
    # create table
    c.execute("""CREATE TABLE repository
                 (
                 filename_fullpath TEXT, 
                 filename TEXT, 
                 extension TEXT, 
                 bytes BLOB                 
                 );
                 """)
                 
    # index table
    
    ## files scoop
    lstFilesFullpath = dcore.search_files.getAllFilesRecursively(['*'], root_dir_to_index)
    
    for file in lstFilesFullpath:
        try:
            (filename, ext) = os.path.splitext(file)
            (path, filename_no_path) = os.path.split(file)
            
            indexFile = False
            for extGlob in options.GLOBS_SEARCH_IN_LONG: #GLOBS_SEARCH_IN_SHORT:
                if fnmatch.fnmatch(file, extGlob):
                    indexFile = True
            
            file_content = None
            if indexFile:
                fh = open(file, 'rb')
                file_content = fh.read()
                throwaway = file_content.decode('utf-8') # raise exception if not ascii: throw file away @@ maybe utf-8?
                fh.close()
            
            # http://stackoverflow.com/questions/3379166/writing-blob-from-sqlite-to-file-using-python
            #cursor.execute("INSERT INTO notes (id, file) VALUES(0, ?)", [sqlite3.Binary(ablob)])
            
            sql_cmd = """INSERT INTO repository
                         VALUES ('%s', '%s', '%s', ?)""" % (file, filename_no_path, ext)
            
            #print(sql_cmd)
            
            if indexFile:
                file_content = file_content.lower() #@@lowercase_bug: well not everything is lower case to help searching :(
                c.execute(sql_cmd, [sqlite3.Binary(file_content)])
            else:
                sql_cmd = sql_cmd.replace('?', 'NULL')
                c.execute(sql_cmd)
                
        except Exception as e:
            print("Error indexing file: '%s': %s." % (file, e))
            #raise e
       
    # save
    conn.commit()
    c.close()
    
    
def __refineSearch(bytes, query):
    """
    @@maybe move out of db
    """

    lines = bytes.splitlines()

    match = []
    lineNo = 1 # lines are typically 1-indexed
    for line in lines:
        line = line.decode()
        if query in line:
            match.append((lineNo, line))
        lineNo += 1
    
    return match
   
def __regexSearch(bytes, query):
    """
    @@maybe move out of db
    """

    lines = bytes.splitlines()

    match = []
    lineNo = 1 # lines are typically 1-indexed
    for line in lines:
        line = line.decode()
        if re.search(query, line, re.IGNORECASE) != None:
            match.append((lineNo, line))
        lineNo += 1
    
    return match
    
def myregexp(expr):
    item = 'test2test'
    reg = re.compile(expr)
    return reg.search(item) is not None

def searchUsingRegexScoopAllThenPyRegex(db_file_fullpath, query):
    print('searchUsingRegexScoopAllThenPyRegex')
    
    # connect
    conn = sqlite3.connect(db_file_fullpath)
    c = conn.cursor()    
    
    # query table
    sql_cmd = """SELECT * FROM repository"""
    print(sql_cmd)
    c.execute(sql_cmd)
    
    for item in c:
        if item[3] is not None:
            try:
                matches = __regexSearch(item[3], query)
                for match in matches:
                    (lineNo, line) = match
                    decorate.printMatch(item[0], lineNo, line)
            except Exception as inst:
                print("Error searching file: '%s': %s." % (item[1], inst))
                #raise
    
def searchUsingRegex(db_file_fullpath, query):
    # @@ regex doesn't work when embed in sqlite :(
    
    print('searchUsingRegex -- NOT SUPPOSED TO BE CALLED - BROKEN'*10)
    
    # connect
    conn = sqlite3.connect(db_file_fullpath)
    conn.create_function("TATA", 1, myregexp)
    c = conn.cursor()    
    
    # query table
    like_clause = "TATA" if isRegex else "LIKE"
    sql_cmd = """SELECT * FROM repository WHERE bytes %s (?)""" % (like_clause)
    print(sql_cmd)
    c.execute(sql_cmd, [('%%%s%%' % query)])
    
    for db_match in c:
        try:
            matches = __refineSearch(db_match[3], query)
            for match in matches:
                (lineNo, line) = match
                decorate.printMatch(db_match[0], lineNo, line)
        except Exception as inst:
            print("Error searching file: '%s': %s." % (db_match[1], inst))
            #raise

def isMatchFilterExt(filename, filterExt):
    
    if len(filterExt) == 0:
        return True
    
    (pre, ext) = os.path.splitext(filename)
    
    if ext in filterExt:
        return True
        
    return False
            
def search(db_file_fullpath, query, filterExt = [], isRegex = False):
    query = query.lower() ## @@a1
    print("db.search (%s, %s)" % (db_file_fullpath, query))
    
    if query is None or query == "":
        print("Inalid query: %s." % query)
        return None
    
    if isRegex:
        return searchUsingRegexScoopAllThenPyRegex(db_file_fullpath, query)
    
    # connect
    conn = sqlite3.connect(db_file_fullpath)
    c = conn.cursor()  
    
    like_clause = "LIKE"
    
    # query table
    sql_cmd = """SELECT * FROM repository WHERE bytes %s (?) COLLATE NOCASE""" % (like_clause)
    print(sql_cmd)
    c.execute(sql_cmd, [('%%%s%%' % query)])
    
    # @@optimize: do extension selection in SQL query, not after fetched all data!
    
    for db_match in c:
        try:
            if isMatchFilterExt(db_match[1], filterExt):
                matches = __refineSearch(db_match[3], query)
                for match in matches:
                    (lineNo, line) = match
                    decorate.printMatch(db_match[0], lineNo, line)
        except Exception as inst:
            print("Error searching file: '%s': %s." % (db_match[1], inst))
            #raise
            
def searchFilename(db_file_fullpath, query, isRegex = False):
    print("db.searchFilename (%s, %s)" % (db_file_fullpath, query))
    
    if isRegex:
        raise Exception("regex not implemented")

    # connect
    conn = sqlite3.connect(db_file_fullpath)
    c = conn.cursor()
    
    # query table
    sql_cmd = """SELECT * FROM repository WHERE filename LIKE '%%%s%%'""" % query
    c.execute(sql_cmd)
    
    for match in c:
        print(match[0])

def searchFilenamePath(db_file_fullpath, query, isRegex = False):
    print("db.searchFilename (%s, %s)" % (db_file_fullpath, query))

    if isRegex:
        raise Exception("regex not implemented")
    
    # connect
    conn = sqlite3.connect(db_file_fullpath)
    c = conn.cursor()
    
    # query table
    sql_cmd = """SELECT * FROM repository WHERE filename_fullpath LIKE '%%%s%%'""" % query
    c.execute(sql_cmd)
    
    for match in c:
        print(match[0])
    
