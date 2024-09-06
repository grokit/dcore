"""
Something new: experimenting with `view`. A view is data derived from notes, meant to be periodically refreshed.

This one: try to find all SQL queries in notes in dump them somewhere in some kind of useful organization.
"""

import shutil
import sys
import os
import argparse
import re
import math
import time

import dcore.osrun as osrun
import dcore.data as dcore_data
import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.meta as meta
import dcore.apps.dnotes.score as score
import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.options as options

_meta_shell_command = 'ns_view_sql'

def _safe_name_as_folder(ss):
    out = []
    for cc in ss:
        if not cc.isalnum():
            out.append('_')
        else:
            out.append(cc)
    return "".join(out)

def _extract_table(ss):
    ss = ss.replace('\n', '').replace('\b', '')
    mm = re.search(
        r'from[ ]*(.*)(where|join|;|group by|order by)',
        ss,
        re.IGNORECASE)
    if mm is not None:
        table_name = mm.groups()[0].replace(
            '\n',
            '').replace(
            r'\z',
            '').replace(
            ' ',
            '').replace(
                '\t',
            '')
        # aa.bb.cc -> cc
        i_d = table_name.rfind('.')
        if i_d != -1 and i_d + 1 < len(table_name):
            table_name = table_name[i_d+1:]
        return table_name
    return None


class SQLQuery:

    def __init__(self, ss):
        self.query = ss.strip()
        self.table_name = _extract_table(ss)

    def __repr__(self):
        out = []
        out.append(f'=' * 40)
        out.append(f'table: {self.table_name}')
        out.append(f'-' * 40)
        out.append(f'{self.query}')
        out.append(f'=' * 40)

        ss = "\n".join(out)
        #ss = ss + ",".join([str(ord(s)) for s in ss])
        return ss


def get_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()


def filter_is_sql_chunk(cc):
    cc = cc.lower()
    i_s = cc.find('select')
    i_f = cc.find('from')
    i_w = cc.find('where')
    if i_f > i_s and i_w > i_f and i_s != -1:
        return True
    return False


def extract():
    out = []

    note_files = util.get_all_note_files()
    for ii, ff in enumerate(note_files):
        try:
            with open(ff, 'r') as fh:
                data = fh.read()
                data = data.split('\n\n')
                data = [dd.strip() for dd in data if len(dd.strip()) > 0 and filter_is_sql_chunk(dd)]
                for cc in data:
                    out.append(SQLQuery(cc))
        except:
            print(f'some issue processing {ff}, likely in {data}')
    return out


def do():
    OUT_VIEW_FOLDER = os.path.join(dcore_data.dcoreTempData(), 'dnote_tmp_views')
    if os.path.exists(OUT_VIEW_FOLDER):
        shutil.rmtree(OUT_VIEW_FOLDER)
    os.makedirs(OUT_VIEW_FOLDER)

    print(f'writing to {OUT_VIEW_FOLDER}')
        
    sql_queries = extract()

    for ss in sql_queries:
        fout = os.path.join(OUT_VIEW_FOLDER, _safe_name_as_folder(str(ss.table_name)))
        if not os.path.exists(fout):
            with open(fout, 'w') as fh:
                fh.write('tmp view begin\n\n')
        with open(fout, 'a') as fh:
            fh.write(str(ss))

if __name__ == '__main__':
    G_ARGS = get_args()

    do()
