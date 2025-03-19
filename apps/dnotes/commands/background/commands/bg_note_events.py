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
    parser.add_argument('-c', '--crawl_and_update', action='store_true', default=False)
    parser.add_argument('-r', '--read', action='store_true', default=True)
    return parser.parse_args()

def add_or_update_time(cursor, uid, ttype, context, now_unixtime_s):
    query = 'SELECT * FROM note_events WHERE uid = ?'
    cursor.execute(query, (uid,))
    result = cursor.fetchone()
    first_seen_unix_s = now_unixtime_s
    last_modified_unix_s = now_unixtime_s
    if result:
        last_uid, last_ttype, last_context, first_seen_unix_s, last_last_modified_unix_s  = result
        # if changed, update last mod
        if (last_uid, last_ttype, last_context) != (uid, ttype, context):
            last_modified_unix_s = now_unixtime_s
        else:
            last_modified_unix_s = last_last_modified_unix_s

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
    for ff in files:
        # this may change too much over time to be useful
        uid = ff
        context = ''
        add_or_update_time(cursor, uid, 'NOTE_FILENAME', context, now_unixtime_s)
    for ff in files:
        # person_id@
        with open(ff, 'r') as fh:
            ii = 0
            for line in fh.readlines():
                # todo: test what happens if have 2 ldaps in same line
                mm = re.search(r'\w+@', line)
                if mm is not None:
                    key = mm.group()
                    context = key
                    # this is not stable, as soon as line changes ... perhaps ok
                    uid = f'{ff}:{ii}-{key}'
                    add_or_update_time(cursor, uid, 'PERSON_ID_MENTION', context, now_unixtime_s)
                ii += 1
        # uuid
        metas = meta.extract(ff, open(ff, 'r').read())
        for mm in metas:
            if mm.meta_type == 'uuid':
                uid = mm.value
                context = ff
                add_or_update_time(cursor, uid, 'UUID', context, now_unixtime_s)
    conn.commit()
    conn.close()

def read(db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # stuff changed since ...
    today = datetime.datetime.today()
    read_cutoff = today.replace(hour=0, minute=0, second=0, microsecond=0)

    query = 'SELECT * FROM note_events WHERE last_modified_unix_s >= ?'
    cursor.execute(query, (int(read_cutoff.timestamp()),))
    results = cursor.fetchall()
    for result in results:
        #uid, ttype, context, first_seen_unix_s, modified_unix_s  = result
        print(result)

if __name__ == '__main__':
    args = get_args()
    db_filename = bg_lib.filename_note_events_db()
    if args.crawl_and_update:
        scan_and_update(db_filename)
        exit(0)
    elif args.read:
        read(db_filename)
        exit(0)
