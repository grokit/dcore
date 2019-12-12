"""
Simple backup script using 7z and default with password encryption.

# BUG(S)

- I think it does not pick up the hidden files (linux) from current directory.
"""

import os
import shutil
import time
import argparse
import getpass

import dcore.files as files
import dcore.private_data as private_data

_meta_shell_command = 'backup_7z'

bin7Zip = r'7z'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--folder_in', default='./', help='Folder to backup.')
    parser.add_argument('-o', '--folder_out', default='./', help='Folder for backup file.')
    parser.add_argument('-n', '--archive_name', default='backup_generic', help='Prefix of archive filename.')
    parser.add_argument('-p', '--ask_for_password', action="store_true")
    args = parser.parse_args()
    return args

def getPW(args):

    pw = None
    if args.ask_for_password:
        keyTag = 'k_custom'
        pw = getpass.getpass('Enter password. input.strip() is applied.\n')
        pw = pw.strip()
    else:
        # Default is to use default pw.
        keyTag = 'k_lsk_scripts_plaintext_07'
        pw = private_data.k_lsk_scripts_plaintext_07

    return pw, keyTag

if __name__ == '__main__':

    args = getArgs()
    pw, keyTag = getPW(args)

    pathToBackup = os.path.abspath(os.path.expanduser(args.folder_in))
    archive_name = files.getUniqueDateFile(args.archive_name, '.%s.7z' % keyTag)
    archive_name = os.path.abspath(os.path.join(args.folder_out, archive_name))

    print('Backup `%s` to `%s`.' % (pathToBackup, archive_name))
    # -mhe: encrypt file names
    # -mx=3: compression level 3 (0:lowest, 9:highest)
    # -v10g: split in 10 gigabytes files
    cmd = f'{bin7Zip} -t7z -mx1 -mhe -p{pw} a {archive_name} "{pathToBackup}"'

    rv = os.system(cmd)
    assert rv == 0

