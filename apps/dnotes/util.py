
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


def version():
    return '0.1.0'

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
    files = []

    files += _walkGatherAllFiles(data.get_notes_root_folder())

    for loc in data.get_notes_folders_ext():
        files += _walkGatherAllFiles(loc)

    files = [ff for ff in files if os.path.splitext(os.path.split(ff)[1])[1] == '.md' ]
    files = list(set(files))

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

def dedup_matches_to_one_per_file(matches):
    dedup = {}
    for m in matches:
        dedup[m.filename] = m

    dedup_matches = []
    for k in dedup:
        dedup_matches.append(dedup[k])
    return dedup_matches
