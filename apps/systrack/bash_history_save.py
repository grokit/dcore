#!/usr/bin/python3
"""
"""

import os
import re
import time
import stat
import getpass
import datetime
import argparse
import sqlite3

import dcore.data as data

_meta_shell_command = 'backup_bash_history'

BASH_HISTORY_LOC = os.path.realpath(os.path.expanduser('~/.bash_history'))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l',
        '--list',
        action="store_true",
        help='List all stored entries.')
    parser.add_argument(
        '-f',
        '--file',
        help=f'Use a specific file to ingest.')
    args = parser.parse_args()
    return args


class BashEntry:
    def __init__(self, unixtime, entry):
        self.unixtime = unixtime
        self.entry = entry


def chomp_till_next(fh):
    acc = []
    while (True):
        pos = fh.tell()
        line = fh.readline()
        if line == "":
            break
        line = line.strip()
        if extract_ts(line) is not None:
            fh.seek(pos)
            break
        acc.append(line)
    return "\n".join(acc)


def extract_ts(line):
    mm = re.search(r'#(\d{10})', line)
    if mm is None:
        return mm
    return int(mm.groups(1)[0])


def read_bash_and_pair_with_time(bash_history_filename):
    acc = []
    with open(bash_history_filename, 'r') as fh:
        while (True):
            unixtime = extract_ts(fh.readline())
            if unixtime is None:
                break
            entry = chomp_till_next(fh)
            acc.append(BashEntry(unixtime, entry))
    return acc


def save_dump_to_sqlite(bash_history_filename):
    bash_history_raw_content = None
    with open(bash_history_filename, 'r') as fh:
        bash_history_raw_content = fh.read().strip()
    db_file = os.path.realpath(
        os.path.join(
            data.dcoreData(),
            'bash_history_save.db'))
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bash_history_dump (
        time TEXT,
        bash_history_raw_content TEXT
    )
    ''')
    timestr = str(datetime.datetime.now().isoformat())
    cursor.execute('''
    DELETE FROM bash_history_dump
    ''')
    cursor.execute('''
    INSERT OR REPLACE INTO bash_history_dump (time, bash_history_raw_content) VALUES (?, ?)
    ''', (timestr, bash_history_raw_content))
    conn.commit()
    conn.close()

def save_individual_entries_to_sqlite(entries):
    db_file = os.path.realpath(
        os.path.join(
            data.dcoreData(),
            'bash_history_save.db'))
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bash_history (
        unixtime INTEGER,
        entry TEXT,
        PRIMARY KEY (unixtime, entry)
    )
    ''')
    for entry in entries:
        cursor.execute('''
        INSERT OR REPLACE INTO bash_history (unixtime, entry) VALUES (?, ?)
        ''', (entry.unixtime, entry.entry))
    conn.commit()
    conn.close()

def do():
    args = get_args()

    if args.list:
        raise Exception("list not implemented")

    bash_history_filename = BASH_HISTORY_LOC
    if args.file:
        bash_history_filename = args.file
        print(f'Using special file {bash_history_filename}.')

    entries = read_bash_and_pair_with_time(bash_history_filename)

    if False:
        dd = set()
        for ee in entries:
            if ee.unixtime in dd:
                print(f'duplicate: {ee.unixtime}')
            dd.add(ee.unixtime)

    if True:
        save_individual_entries_to_sqlite(entries)
        save_dump_to_sqlite(bash_history_filename)

if __name__ == '__main__':
    do()
