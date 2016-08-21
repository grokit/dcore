
import os
import shutil
import time

import dcore.files as files
import dcore.private_data as private_data

_meta_shell_command = 'backup'

#backup_in = r'/media/usbd'
backup_in = r'/media/arch/f5252dc7-fbae-4c98-9a5e-58988d4936d3'
backup_path = r'~/'

bin7Zip = r'7z'

if __name__ == '__main__':
    pathToBackup = os.path.expanduser(backup_path)
    
    archive_name = files.getUniqueDateFile('backup_generic_', '.k_lsk-01.7z')
    archive_name = os.path.join(backup_in, archive_name)
     
    pw = private_data.k_lsk_scripts_plaintext_01
    
    # -mhe: encrypt file names
    # -mx=3: compression level 3 (0:lowest, 9:highest)
    encrypt = True
    if encrypt:
        cmd = '%s -t7z -mx1 -mhe -p%s a %s "%s"' % (bin7Zip, pw, archive_name, pathToBackup)
    else:
        raise Expcetion("Not coded.")

    print(cmd)
    os.system(cmd)
