"""
Simple backup script using 7z and default with password encryption.
"""

import os
import shutil
import time
import argparse
import getpass

import dcore.files as files
import dcore.private_data as private_data

_meta_shell_command = 'backup'

bin7Zip = r'7z'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--folder_in', default='./', help='Folder to backup.')
    parser.add_argument('-o', '--folder_out', default='./', help='Folder for backup file.')
    parser.add_argument('-n', '--archive_name', default='backup_generic', help='Prefix of archive filename.')
    parser.add_argument('-p', '--ask_for_password', action="store_true")
    args = parser.parse_args()
    return args

def getPW():
    pw = None
    try:
        # If private data is set, use default password.
        pw = private_data.k_lsk_scripts_plaintext_02
        keyTag = 'k_lsk-02'
    except Exception as e:
        pass

    if pw is None or args.ask_for_password:
        pw = getpass.getpass('Enter password. input.strip() is applied.\n')
        pw = pw.strip()
        keyTag = 'k_custom'

    return pw, keyTag

if __name__ == '__main__':

    args = getArgs()
    pw, keyTag = getPW()

    pathToBackup = os.path.expanduser(args.folder_in)
    archive_name = files.getUniqueDateFile(args.archive_name, '.%s.7z' % keyTag)
    archive_name = os.path.join(args.folder_out, archive_name)

    # -mhe: encrypt file names
    # -mx=3: compression level 3 (0:lowest, 9:highest)
    encrypt = True
    if encrypt:
        cmd = '%s -t7z -mx2 -mhe -p%s a %s "%s"' % (bin7Zip, pw, archive_name, pathToBackup)
    else:
        raise Expcetion("Not coded.")

    os.system(cmd)
