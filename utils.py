import datetime
import os

import dcore.data as data

def dateForAnnotation():
    return datetime.datetime.now().isoformat()

def delCurrentShortcuts(tag):
    "Delete all files that have special marker inside output directory."
    scriptsOutputFolder = data.pathExt()
    
    for f in os.listdir(scriptsOutputFolder):
        f = os.path.join(scriptsOutputFolder, f)
        with open(f, 'r') as fh:
            fdata = fh.read()
        if tag in fdata:
            # print('Deleting script shortcut: %s.' % f)
            os.remove(f)

def insert_cut(filename, cut_marker_start, cut_marker_end, to_insert_list, clobber=False):
    """
    clobber=True: erase what was previously between the markers.

    returns: the whole file as string with the proper insertion.
    """

    lines = []
    cut = []
    for i, line in enumerate(open(filename, 'r').readlines()):
        if cut_marker_start in line:
            cut.append(i)
        if cut_marker_end in line:
            assert i > 0
            cut.append(i)
        lines.append(line)
    assert len(cut) == 2
    assert cut[1] > cut[0]

    if clobber:
        lines = lines[0:cut[0]+1] + to_insert_list + lines[cut[1]:]
    else:
        lines = lines[0:cut[0]+1] + to_insert_list + lines[cut[0]+1:]

    return "".join(lines)



def open_file_autoselect_app(filename):
    app = 'xdg-open'
    if os.path.splitext(filename)[1] in set(['.webm', '.mp4']):
        app = 'mpv'
    elif os.path.splitext(filename)[1] in set(['.md', '.txt']):
        # vi: would need to fix console issues
        # app = 'vi'
        pass
    elif os.path.splitext(filename)[1] == '.pdf':
        app = 'okular'
    else:
        app = 'gio open'
    cmd = f'{app} {filename}& >/dev/null 2>&1' 
    print(cmd)
    os.system(cmd)
