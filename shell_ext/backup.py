
import os
import shutil
import time

import dcore.osext as osext
import dcore.files as files
import dcore.system_description as private_data

_meta_shell_command = '__DEPRECATED_backup'

backup_in = r'T:\backups\auto'

# disable for now
# to_backup_online = r'C:\david\sync\skydrive'

exe_7zip = r'c:\david\app\7zip\7z.exe'

if __name__ == '__main__':
    backup_loc = os.path.abspath('.')
    
    os.chdir(backup_in)

    archive_name = files.getUniqueDateFile('backup_generic_', '.k0.7z')
     
    # -mhe: encrypt file names
    pw = private_data.sk0
    cmd = '%s -t7z -mhe -p%s a %s "%s"' % (exe_7zip, pw, archive_name, backup_loc)

    print(cmd)
    os.system(cmd)

    cmd = r'copy ' + archive_name + ' ' + to_backup_online + '\\' + archive_name
    print(cmd)
    os.system(cmd)
    
    
