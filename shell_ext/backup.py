
import os
import shutil
import time

import dcore.osext as osext
import dcore.files as files
import dcore.system_description as private_data

_meta_shell_command = 'backup'

backup_in = r'/media/usbd'
backup_path = r'~/sync'

#exe_7zip = r'c:\david\app\7zip\7z.exe'
exe_7zip = r'7z'

if __name__ == '__main__':
    pathToBackup = os.path.expanduser(backup_path)
    
    #os.chdir(backup_in)

    archive_name = files.getUniqueDateFile('backup_generic_', '.k0.7z')
    archive_name = os.path.join(backup_in, archive_name)
     
    # -mhe: encrypt file names
    # -mx=3: compression level 3 (0:lowest, 9:highest)
    pw = private_data.k_lsk_scripts_plaintext_01
    cmd = '%s -t7z -mx1 -mhe -p%s a %s "%s"' % (exe_7zip, pw, archive_name, pathToBackup)

    print(cmd)
    os.system(cmd)
    
