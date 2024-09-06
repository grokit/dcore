"""
"""
import os

_meta_shell_command = 'td'

if __name__ == '__main__':
    if os.name == 'nt':
        cmd = 'ns -O uuid:::windows_todo'
    else:
        cmd = 'ns -O uuid:::todo_r554'
    os.system(cmd)
