"""
todo:::a1
- crawl all .md files
- extract something very simple like id@
- store as/with uid
- allow to list in last x days (new or last mod)
"""

import shutil
import sys
import os
import argparse
import re
import math
import time
import sqlite3
import datetime
import hashlib

import dcore.osrun as osrun
import dcore.data as dcore_data
import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.meta as meta
import dcore.apps.dnotes.score as score
import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.options as options
import dcore.apps.dnotes.commands.background.bg_lib as bg_lib

_meta_shell_command = 'bg_note_events'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--crawl_and_update',
        action='store_true',
        default=False)
    parser.add_argument('-r', '--read', action='store_true', default=True)
    parser.add_argument('--reset', action='store_true', default=False)
    return parser.parse_args()


def quick_short_hash(ss):
    length = 12
    return hashlib.sha256(ss.encode()).hexdigest()[:length]

def add_or_update_time(cursor, uid, ttype, context,
                       last_observed_change_unixtime_s):
    query = 'SELECT * FROM note_events WHERE uid = ?'
    cursor.execute(query, (uid,))
    result = cursor.fetchone()
    first_seen_unix_s = last_observed_change_unixtime_s
    last_modified_unix_s = last_observed_change_unixtime_s
    if result:
        _last_uid, _last_ttype, _last_context, _first_seen_unix_s, _last_modified_unix_s = result
        # preserve first seen
        first_seen_unix_s = _first_seen_unix_s
        # only update last_modified_unix_s if there is a change (rely mainly on context)
        if (_last_uid, _last_ttype, _last_context) != (uid, ttype, context):
            last_modified_unix_s = last_observed_change_unixtime_s
        else:
            last_modified_unix_s = _last_modified_unix_s

    dml = f'''
    INSERT OR REPLACE INTO note_events VALUES (?, ?, ?, ?, ?)
    '''
    cursor.execute(
        dml,
        (uid,
         ttype,
         context,
         first_seen_unix_s,
         last_modified_unix_s))


def last_changed_unixtime_s(filepath):
    return int(os.path.getmtime(filepath))


def generic_regex_and_line_marker(cursor, regex, ff, ttype):
    last_changed_u_s = last_changed_unixtime_s(ff)
    with open(ff, 'r') as fh:
        ii = 0
        for line in fh.readlines():
            mm = re.search(regex, line)
            if mm is not None:
                key = mm.group()
                # hash(line) makes sense: only update if the line
                # if mentioned >1 in same file with no or same line, eh fine to only track once
                uid = f'{ff}-{quick_short_hash(line)}-{key}'
                context = line.strip()
                add_or_update_time(
                    cursor,
                    uid,
                    ttype,
                    context,
                    last_changed_u_s)
            ii += 1

def scan_and_update(db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS note_events (
        uid TEXT,
        type TEXT,
        context TEXT,
        first_seen_unix_s INTEGER,
        last_modified_unix_s INTEGER,
        PRIMARY KEY (uid)
    )
    ''')

    now_unixtime_s = int(time.time())
    files = sorted(util.get_all_note_files())
    if False:
        files = ['']
    for ff in files:
        last_changed_u_s = last_changed_unixtime_s(ff)
        # this may change too much over time to be useful
        uid = ff
        context = last_changed_u_s
        add_or_update_time(
            cursor,
            uid,
            'NOTE_FILENAME',
            context,
            last_changed_u_s)
    for ff in files:
        # ldap-like my_name@ or my_name@something.com
        generic_regex_and_line_marker(cursor, r'\w+@', ff, 'PERSON_ID_MENTION')
        # https://wwww.geico.com
        generic_regex_and_line_marker(cursor, r'\w+://[^\s\n]+', ff, 'URL')
        # go/abcd-efg
        generic_regex_and_line_marker(cursor, r'go/\w+', ff, 'GO_SLASH')
        # b/12345
        generic_regex_and_line_marker(cursor, r'b/[0-9]+', ff, 'B_SLASH')
        # uuid
        metas = meta.extract(ff, open(ff, 'r').read())
        for mm in metas:
            if mm.meta_type == 'uuid':
                uid = mm.value
                context = ff
                add_or_update_time(
                    cursor, uid, 'UUID', context, last_changed_u_s)
    conn.commit()
    conn.close()


def read(db_filename):
    """
    TODO:
    - break down and indicate the day as yyyy-mm-dd
    - better render
    """
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # stuff changed since ...
    if True:
        read_cutoff = ( datetime.datetime.today() - datetime.timedelta(days=2)).replace( hour=0, minute=0, second=0, microsecond=0)
    else:
        read_cutoff = ( datetime.datetime.today() - datetime.timedelta(hours=1))

    query = 'SELECT * FROM note_events WHERE last_modified_unix_s >= ?'
    cursor.execute(query, (int(read_cutoff.timestamp()),))
    results = cursor.fetchall()

    # sort by last_modified_unix_s
    column_names = [desc[0] for desc in cursor.description]
    ii = column_names.index('last_modified_unix_s')
    results = sorted(results, key=lambda x: x[ii])

    print(column_names)
    for result in results:
        # uid, ttype, context, first_seen_unix_s, modified_unix_s  = result
        print(result)


if __name__ == '__main__':
    args = get_args()
    db_filename = bg_lib.filename_note_events_db()
    if args.reset:
        conn = sqlite3.connect(db_filename)
        conn.cursor().execute('DROP TABLE note_events')
        exit(0)
    if args.crawl_and_update:
        scan_and_update(db_filename)
        exit(0)
    elif args.read:
        read(db_filename)
        exit(0)
