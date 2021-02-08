
import os
import platform

import dcore.apps.dnotes.data as data

def _walkGatherAllFiles(rootdir='.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append(os.path.join(dirpath, f))
    return F

################################################################################
# PUBLIC
################################################################################

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


