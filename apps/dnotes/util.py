
import os
import platform

import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.meta as meta

def _walkGatherAllFiles(rootdir='.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append(os.path.join(dirpath, f))
    return F

################################################################################
# PUBLIC
################################################################################


def select_filename_by_uuid(uuid):
    files = get_all_note_files()

    filename = None
    for ff in files:
        metas = meta.extract(ff, open(ff).read())
        for mm in metas:
            if mm.meta_type == 'uuid':
                if mm.value == uuid:
                    assert filename is None
                    filename = mm.source_filename
    assert filename is not None
    return filename


def manualSelectMatchesScores(matches, scores, nCut=30):
    """
    TODO: generalize to just select n things, not just match/scores. Merge with manualSelect(_) below.
    """

    print(
        'Select an item by entering its corresponding number. Enter cancels.')
    i = 0

    if len(matches) > nCut:
        matches = matches[0:nCut]
        print('Too many matches, cutting down to %s.' % len(matches))

    for i in range(len(matches)):
        print('%.2d (%.2f): %s' % (i, scores[i], matches[i].filename))

    s = input()
    if len(s) == 0: return None
    s = int(s)

    return matches[s]

def manualSelect(str_list, nCut=30):

    print(
        'Select an item by entering its corresponding number. Enter cancels.')
    i = 0

    if len(str_list) > nCut:
        matches = matches[0:nCut]
        print('Too many matches, cutting down to %s.' % len(str_list))

    for i in range(len(str_list)):
        print('%.2d: %s' % (i, str_list[i]))

    s = input()
    if len(s) == 0: return None
    s = int(s)

    return str_list[s]

def get_all_note_files():
    files = _walkGatherAllFiles(data.get_notes_root_folder())
    files = [ f for f in files if os.path.splitext(os.path.split(f)[1])[1] == '.md' ]
    # TODO: *might* consider removing files from get_notes_archive_folder() (if gets slow or noisy).
    return files

def createFolderIfNotExist(folder):
    if not os.path.isdir(folder):
        print('Folder does not exist, creating.')
        os.makedirs(folder)

def createFileIfNotExist(file):
    if not os.path.isfile(file):
        print('File does not exist, creating.')
        with open(file, 'w') as fh:
            fh.write('')

def openInEditor(noteFilename):
    if platform.system() == 'Windows':
        cmd = 'notepad %s' % noteFilename
    else:
        cmd = 'vi %s' % noteFilename
    rs = os.system(cmd)
    assert rs == 0


