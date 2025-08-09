"""
Note: the official dir for this is in dcore, need to run dcore/install.py to copy it to vi's directory.
Because of that, move all logic to vim_extension.
"""

import dcore.apps.vim_extension.vim_extension as vim_extension

def open_link():
    return vim_extension.open_link()

def test_print():
    print('hello vim')

def notify_file_opened_or_created():
    return vim_extension.notify_file_opened_or_created()

if __name__ == '__main__':
    pass

