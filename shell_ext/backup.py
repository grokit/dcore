import os
import shutil
import time

import misc.osext as osext
import misc.files
import dcore.private_data as private_data

_meta_shell_command = 'backup'

backup_in = r'T:\backups\auto'

to_backup_online = r'C:\david\sync\skydrive'

exe_7zip = r'c:\david\sync\app\7zip\7z.exe'

if __name__ == '__main__':
    backup_loc = os.path.abspath('.')
    
    os.chdir(backup_in)

    archive_name = misc.files.getUniqueDateFile('backup_generic_', '.k0.7z')
     
    # -mhe: encrypt file names
    pw = private_data.lsk0
    cmd = '%s -t7z -mhe -p%s a %s "%s"' % (exe_7zip, pw, archive_name, backup_loc)

    print(cmd)
    os.system(cmd)

    cmd = r'copy ' + archive_name + ' ' + to_backup_online + '\\' + archive_name
    print(cmd)
    os.system(cmd)
    
    
