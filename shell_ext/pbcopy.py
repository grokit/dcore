
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

def fromStdInIfDataTolerateBinary():
    """
    Workaround for when binary data in stdin. E.g.:

        return sys.stdin.read()
        File "/usr/lib/python3.7/codecs.py", line 322, in decode
        (result, consumed) = self._buffer_decode(data, self.errors, final)
        UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe8 in position 1049: invalid continuation byte
    """

    with open(sys.stdin.fileno(), mode='rb', closefd=False) as fh:
        data = fh.read()
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        print('Warning: some binary data in stdin, hacky-fix input applied.')
        out = []
        for d in data:
            d = int(d)
            if d >= 0 and d <= 126:
                out.append(chr(d))
            else:
                out.append('[?clipb-removed?]')
        return "".join(out)


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
    data = fromStdInIfDataTolerateBinary().strip()
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

