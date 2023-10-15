"""
Like the good old cls.exe of windows.

Also insert a delimiter to allow splitting shell output history.
"""

import os

import dcore.data as data

_meta_shell_command = 'cls'

if __name__ == '__main__':
    for i in range(200):
        print('')
    print(data.cls_file_delimiter())

