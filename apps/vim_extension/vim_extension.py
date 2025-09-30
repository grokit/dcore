import vim
import webbrowser
import os
import logging
import uuid
import string

import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.options as options
import dcore.dlogging as dlogging
import dcore.data as data
import dcore.utils as dutils
import dcore.kvp_store as kvp_store
import dcore.apps.quickdir.lib as quickdir_lib

"""
vim.current.buffer.append('This would get added at cursor.')

run command, return result to python:
vim.eval('command')

execute a vim command (in this case opens file.txt):
vim.command(':e file.txt')

note: could open at a specific line using:
    vi +12 file.ext
    ... for line 12
"""

def get_curr_line():
    row, col = vim.current.window.cursor
    return vim.current.buffer[row-1]

def get_curr_word():
    row, col = vim.current.window.cursor
    line = vim.current.buffer[row-1]
    if line[col] == ' ': return ''
    i_left = 0
    i_right = len(line)

    sep = set([' ', '\t'])
    for j in range(col, len(line)):
        if line[j] in sep: break
        i_right = j+1

    for j in range(col, -1, -1):
        if line[j] in sep: break
        i_left = j

    return line[i_left:i_right]

def _extract_link_remove_undesired(ww):
    # Don't mess with URLs (they may have paren & cie).
    if ww.startswith('http'):
        return ww

    # for uid, it would be MUCH better to just expand left/right
    # from cursor on allowed chars instead of guess games
    # (but see TODO: use parse lib instead of in this file)
    # ... then can remove this for other types of links (e.g. url)
    # what about pre/shortcut types though?
    # (would probably want similar sub-behavior based on type)
    if ww[0] == '(':
        ww = ww[1:]
    if ww[-1] == ')':
        ww = ww[0:-1]
    if ww[0] == '[':
        ww = ww[1:]
    if ww[-1] == ']':
        ww = ww[0:-1]

    return ww

def _filter_meta_value(ww):
    allowed = set(string.ascii_letters + string.digits + '_-')
    i = len(ww)
    for j in range(0, len(ww)):
        if ww[j] not in allowed:
            i = j
            break
    ww = ww[0:i]
    return ww

def open_link():
    word = get_curr_word().strip()
    word_ = _extract_link_remove_undesired(word)
    print(f'got v5: `{word}` -> {word_}')
    word = word_
    del word_

    filenames_matched = []
    if options.MSEP in word:
        # TODO: use official parse lib for this instead of ad-hoc
        # ... this would also get rid
        compound = word.split(options.MSEP)
        if len(compound) == 2:
            meta_key, meta_value = compound
            # replace link types to targets
            if meta_key == 'luid':
                meta_key = 'uuid'
            if meta_key == 'lloc':
                meta_key = 'loc'
            meta_value_ = _filter_meta_value(meta_value)
            #print(f'meta-filter: {meta_key} / {meta_value} -> {meta_value_}')
            meta_value = meta_value_
            del meta_value_
            filenames_matched += search.get_filenames_matching_meta_key_and_value(meta_key, meta_value)

    matched_once = False
    #print(filenames_matched)
    for filename, line_no in filenames_matched:
        vim.command(f':silent! | :tabe {filename} | :{line_no+1}')
        matched_once = True

    if not matched_once:
        if len(word.split('/')) == 2:
            pre, post = word.split('/')
            if pre in set(['go', 'b', 'cl']):
                webbrowser.open(f'http://{word}')
                matched_once = True

    if not matched_once:
        if word.startswith('http://') or word.startswith('https://') or word.startswith('chrome://'):
            webbrowser.open(f'{word}')
            matched_once = True

    if not matched_once:
        if word[0:5] == 'b/hot':
            webbrowser.open(f'http://{word}')
            matched_once = True

def test_print():
    print('hello vim')

def notify_file_opened_or_created():
    """
    Called from vim plugin, careful if rename.
    """
    filename_log = os.path.join(data.dcoreTempData(), 'vi_files_opened.log')
    filename = vim.current.buffer.name

    date_annot = dutils.date_now_for_annotation()
    to_write = f'{date_annot} {filename}\n'
    with open(filename_log, 'a') as fh:
        fh.write(to_write)
    # experimental -- just write data there, can remove later
    key = str(uuid.uuid1()).replace('-','_')
    kvp_store.write(key, to_write, namespace='vi_operations')
    filename_path = os.path.dirname(filename)
    # quick access to last path
    quickdir_lib.remember_dir_typed(quickdir_lib.DirShortcut(path=filename_path,shortcut='vl'))

if __name__ == '__main__':
    pass

