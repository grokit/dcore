"""
Experimental: daily digest.
"""

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

_meta_shell_command = 'bg_daily_digest'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',
                        '--aaa',
                        action='store_true',
                        help='...')
    return parser.parse_args()


def do():
    today_str = datetime.datetime.today().strftime('%Y-%m-%d')
    folder_out = os.path.join(dcore_data.dcoreTempData(), f'dnote_daily_digest', f'{today_str}')
    if os.path.exists(folder_out):
        return
    print(f'daily digest not present, triggering in {folder_out}')
    os.makedirs(folder_out)

    files = util.get_all_note_files()

    filename_out = os.path.join(folder_out, 'all_files.json')
    with open(filename_out, 'w') as fh:
        fh.write(json.dumps(files, indent=4))

    filename_out = os.path.join(folder_out, 'all_metas.json')
    meta_s = []
    uuid_s = []
    for ff in files:
        metas = meta.extract(ff, open(ff, 'r').read())
        for mm in metas:
            meta_s.append((mm.meta_type, mm.value, mm.source_filename))
            if mm.meta_type == 'uuid':
                uuid_s.append((mm.source_filename, mm.value))
    with open(filename_out, 'w') as fh:
        fh.write(json.dumps(meta_s, indent=4))

    filename_out = os.path.join(folder_out, 'all_uuids.json')
    with open(filename_out, 'w') as fh:
        fh.write(json.dumps(uuid_s, indent=4))

if __name__ == '__main__':
    G_ARGS = get_args()
    do()
