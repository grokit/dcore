
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

def clipFilenameContent(filename):
    if platform.system() in ["macosx", "Darwin"]:
        cmd = 'pbcopy < %s'
    else:
        cmd = 'xclip -selection clipboard < %s'
    cmd = cmd % filename
    print(cmd)
    os.system(cmd)

def fromStdInIfData():
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?');
    args = parser.parse_args()

    if args.filename:
        print(f'Reading from {args.filename}.')
        clipFilenameContent(args.filename)
        sys.exit(0)

    # TemporaryFile is better, but f.name attribute not 
    # available.
    # See https://docs.python.org/3/library/tempfile.html
    data = fromStdInIfData().strip()
    if True:
        with tempfile.NamedTemporaryFile('w') as fh:
            # Works fine, but a bit hacky
            pos = fh.write(data)
            fh.flush() # if you don't flush, file might be empty
            clipFilenameContent(fh.name)

            # Be super safe, wipe data before close file.
            fh.seek(0)
            fh.write('0' * 2 * pos)

    else:
        # Does not work on all systems.
        clip(data)

    
