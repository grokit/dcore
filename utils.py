import datetime
import importlib.util
import inspect
import os
import platform

import dcore.data as data

################################################################################
# DATE STUFF
################################################################################

def __date_safeset(ss):
    _SAFESET = set('0123456789-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    out = []
    for cc in ss:
        if cc in _SAFESET:
            out.append(cc)
        else:
            out.append('_')
    return "".join(out)

def date_now_for_annotation():
    return datetime.datetime.now().isoformat()

def date_now_iso_8601_safe_folder():
    return __date_safeset(datetime.datetime.now().astimezone().isoformat())

################################################################################
# ...
################################################################################

def filename_aggresive_simplify(filename):
    """
    Replace chars in filename that can cause problems in some systems.
    """

    non_alphanum_allowed = set( '._-')  # ()[]

    accents_to_set = {
        'ä': 'a',
        'à': 'a',
        'â': 'a',
        '&': 'and',
        'é': 'e',
        'ê': 'e',
        'è': 'e',
        'ë': 'e',
        'ô': 'o',
        'ç': 'c',
        'Ä': 'A',
        'À': 'A',
        'Â': 'A',
        'É': 'E',
        'È': 'E',
        'Ô': 'O',
        'Ç': 'C',
    }

    toLower = True

    fout = []
    for ll in filename:
        if (ll.isalnum() and ll.isascii()) or ll in non_alphanum_allowed:
            fout.append(ll)
        else:
            if ll in accents_to_set:
                fout.append(accents_to_set[ll])
            else:
                fout.append('_')

    if toLower:
        for i in range(0, len(fout)):
            fout[i] = fout[i].lower()

    ss = "".join(fout)
    while '__' in ss:
        ss = ss.replace('__', '_')
    while '_.' in ss:
        ss = ss.replace('_.', '.')
    ss = ss.strip('-_')
    return ss

def portableCharacterSet():
    """
    3.282 Portable Filename Character Set
    https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_282

    TODO?: replace __date_safeset?
    """
    return set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-')

def extractFunctionsDictFromFilename(filepath):
    spec = importlib.util.spec_from_file_location("module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    functions = {function_name: fn for function_name, fn in module.__dict__.items() if callable(fn)}
    return functions

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
    # app = 'gio open'
    app = 'xdg-open'
    if os.path.splitext(filename)[1] in set(['.webm', '.mp4']):
        app = 'mpv'
    elif os.path.splitext(filename)[1] in set(['.md', '.txt']):
        # vi: would need to fix console issues
        # app = 'vi'
        pass
    elif os.path.splitext(filename)[1] == '.pdf':
        app = 'okular'
    cmd = f"{app} '{filename}'& >/dev/null 2>&1" 
    print(cmd)
    os.system(cmd)


def openInEditor(noteFilename):
    if platform.system() == 'Windows':
        cmd = 'notepad %s' % noteFilename
    else:
        cmd = 'vi %s' % noteFilename
    rs = os.system(cmd)
    assert rs == 0

