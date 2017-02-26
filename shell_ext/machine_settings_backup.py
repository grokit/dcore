"""

save_machine_settings -w: wipe 
save_machine_settings -r: restore
save_machine_settings -s: save (default)

wipe and restore should save current settings as precaution
"""

import os
import zipfile

# Can be eiter file or folder, backup will act accordingly.
TO_SAVE = [
    '~/.gdbinit',
    '~/.inputrc',
    '~/.bashrc',
    '~/.bash_history',
    '~/.tmux.conf',
    '~/.vimrc',
    '~/.vim',
]

# TODO: import from dcore if there.
ARCHIVE_PASSWORD = 'fslw87d6t74wqabtqtfss2zphidh4m8hyboskf04aom21b73u9ghnzm0ior5xm71'

def pathFix(p):
    return os.path.abspath(os.path.expanduser(p))

def getTarget():
    return './machine_settings.zip'

def foldetToFileSet(rootdir):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append(os.path.normpath(os.path.join(dirpath, f)))
    return F

def expandFileAndFolderSet(ffs):
    ffsO = []
    for f in ffs:
        if os.path.isfile(f):
            ffsO.append(f)
        elif os.path.isdir(f):
            for fExp in foldetToFileSet(f):
                ffsO.append(fExp)
        else:
            raise Exception("Bad file or folder: %s." % f)
    return ffsO

def backupTo(archiveTarget, filesAndFolderSet):
    with zipfile.ZipFile(archiveTarget, 'w') as archive:
        #archive.setpassword(PASSWORD)
        for f in expandFileAndFolderSet(filesAndFolderSet):
            archive.write(f)

if __name__ == '__main__':
    to_save = TO_SAVE
    to_save = [pathFix(p) for p in to_save] 
    to_save_filtered = [p for p in to_save if (os.path.isfile(p) or os.path.isdir(p))] 

    backupTo(pathFix('~/backup_settings.zip'), to_save_filtered)
        
