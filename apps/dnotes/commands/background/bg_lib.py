"""
Experimental: daily digest.

# TODO

## As

- pickle makes it hard to edit, and need all definition in caller

## Bs

"""

import sqlite3
import json
import pickle
import dataclasses
import sys
import os
import shutil
import argparse
import datetime
import re
import math
import time
import json

import dcore.osrun as osrun
import dcore.data as dcore_data
import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.meta as meta
import dcore.apps.dnotes.score as score
import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.options as options

################################################################################
# DATA
################################################################################

@dataclasses.dataclass
class UuidWithMeta:
    uuid: str
    filename: str

################################################################################
# FILES AND FOLDERS
################################################################################

def daily_folder_out():
    today_str = datetime.datetime.today().strftime('%Y-%m-%d')
    return os.path.join(
        dcore_data.dcoreTempData(),
        f'dnote_backgound_tasks',
        f'daily_digest',
        f'{today_str}')

def permament_folder_out():
    return os.path.join(
        dcore_data.dcoreTempData(),
        f'dnote_backgound_tasks',
        f'permanent')

def filename_uuid_db():
    return os.path.join(permament_folder_out(), 'uuids_db.pickle')

################################################################################
# ...
################################################################################

def daily_digest():
    folder_out = daily_folder_out()
    if os.path.exists(folder_out):
        if True:
            return
        else:
            shutil.rmtree(folder_out)

    print(f'daily digest not present, triggering in {folder_out}')
    os.makedirs(folder_out)

    files = util.get_all_note_files()

    filename_out = os.path.join(folder_out, 'all_files.json')
    with open(filename_out, 'w') as fh:
        fh.write(json.dumps(files, indent=4))

    meta_s = []
    uuid_s = []
    now_s = []
    for ff in files:
        metas = meta.extract(ff, open(ff, 'r').read())
        for mm in metas:
            meta_s.append((mm.meta_type, mm.value, mm.source_filename))
            if mm.meta_type == 'uuid':
                uuid_s.append((mm.source_filename, mm.value))
            if mm.meta_type == 'tag' and mm.value == 'now':
                now_s.append((mm.source_filename, mm.value))

    filename_out = os.path.join(folder_out, 'all_metas.json')
    with open(filename_out, 'w') as fh:
        fh.write(json.dumps(meta_s, indent=4))

    filename_out = os.path.join(folder_out, 'all_uuids.json')
    with open(filename_out, 'w') as fh:
        fh.write(json.dumps(uuid_s, indent=4))

    filename_out = os.path.join(folder_out, 'all_now.json')
    with open(filename_out, 'w') as fh:
        fh.write(json.dumps(now_s, indent=4))


def uuids_extract_from_notes_and_check_dupl():
    uuids_map = {}
    files = sorted(util.get_all_note_files())
    for ff in files:
        metas = meta.extract(ff, open(ff, 'r').read())
        for mm in metas:
            if mm.meta_type == 'uuid':
                uobj = UuidWithMeta(uuid=mm.value, filename=ff)
                if mm.value in uuids_map:
                    print(f'conflict: {uuids_map[mm.value]} / {uobj}')
                    assert mm.value not in uuids_map
                uuids_map[mm.value] = uobj

    return list(uuids_map.values())

def uuids_extract_from_db():
    """
    List of uuids last time we did a sweep.
    """
    folder_out = permament_folder_out()
    if not os.path.exists(folder_out):
        os.makedirs(folder_out)
    filename = filename_uuid_db()
    if not os.path.exists(filename):
        return []
    with open(filename, 'rb') as fh:
        print(f'reading {filename}')
        data = fh.read()
    return pickle.loads(data)

def merge_uuids(last, current):
    assert current is not None
    if last == None: return current
    # both last and current: here we could merge or update
    # in the future
    return current

def uuids_to_db():
    uuids_last = uuids_extract_from_db()

    uuids_merged = {}
    for uuid in uuids_last:
        assert uuid.uuid not in uuids_merged
        uuids_merged[uuid.uuid] = uuid

    uuids_notes = uuids_extract_from_notes_and_check_dupl()

    if True:
        uuids_in_notes = set()
        for uwm in uuids_notes:
            uuids_in_notes.add(uwm.uuid)
        # check if in last but not current (throw -- should never lose a uuid)
        for uwm in uuids_last:
            if uwm.uuid not in uuids_in_notes:
                print(f'ERROR: missing {uwm}')
                assert uwm.uuid in uuids_in_notes 

    # merge in notes / update existing
    for uuid in uuids_notes:
        last = uuids_merged.get(uuid.uuid, None)
        uuids_merged[uuid.uuid] = merge_uuids(last, uuid)

    filename = filename_uuid_db()
    data = pickle.dumps(list(uuids_merged.values()))
    with open(filename, 'wb') as fh:
        print(f'wrote to {filename}')
        fh.write(data)

if __name__ == '__main__':
    # just for testing, eventually delete
    uuids_to_db()
