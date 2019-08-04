
_meta_shell_command = 'clipb'

import sys
import os
import argparse
import tempfile
import platform

def clip(data):
    """
    Does not work on Linux :/
    """
    from tkinter import Tk
    tk = Tk()
    tk.withdraw()
    tk.clipboard_clear()
    tk.clipboard_append(data)
    if False:
        # not sure if needed
        tk.update() 
        tk.destroy()
    tk.after(500, tk.destroy)
    tk.mainloop()

def fromStdInIfData():
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    # TemporaryFile is better, but f.name attribute not 
    # available.
    # See https://docs.python.org/3/library/tempfile.html
    with tempfile.NamedTemporaryFile('w') as fh:
        if True:
            # Works fine, but a bit hacky
            fh.write(fromStdInIfData())
            fh.flush() # if you don't flush, file might be empty
            if platform.system() in ["macosx", "Darwin"]:
                cmd = 'pbcopy < %s'
            else:
                cmd = 'xclip -selection clipboard < %s'
            cmd = cmd % fh.name
            os.system(cmd)
        else:
            # Does not work on all systems.
            clip(fromStdInIfData())

    
