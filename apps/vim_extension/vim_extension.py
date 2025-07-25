import vim
import webbrowser

import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.options as options

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

def _remove_paren(ww):
    # Don't mess with URLs (they may have paren & cie).
    if ww.startswith('http'):
        return ww

    if ww[0] == '(':
        ww = ww[1:]
    if ww[-1] == ')':
        ww = ww[0:-1]
    if ww[0] == '[':
        ww = ww[1:]
    if ww[-1] == ']':
        ww = ww[0:-1]

    if ')' in ww:
        ww = ww[0:ww.find(')')]

    return ww

def open_link():
    word = get_curr_word().strip()
    print(f'got v2: `{word}` -> {_remove_paren(word)}')
    word = _remove_paren(word)

    filenames_matched = []
    if options.MSEP in word:
        compound = word.split(options.MSEP)
        if len(compound) == 2:
            meta_key, meta_value = compound
            # replace link types to targets
            if meta_key == 'luid':
                meta_key = 'uuid'
            if meta_key == 'lloc':
                meta_key = 'loc'
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
        if word[0:7] == 'http://' or word[0:8] == 'https://':
            webbrowser.open(f'{word}')
            matched_once = True

    if not matched_once:
        if word[0:5] == 'b/hot':
            webbrowser.open(f'http://{word}')
            matched_once = True

def test_print():
    print('hello vim')

if __name__ == '__main__':
    pass

