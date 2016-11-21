"""
MailR: Mail Read. Receive mail using pre-configured (username, pw) on machine.
"""

import argparse
import time
import base64
import sys

import dcore.private_data as private_data
import dcore.apps.gmail.gmail as gmail

_meta_shell_command = 'mailr'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_mail_read', default=10, type=int)
    args = parser.parse_args()
    return args
    
if __name__ == '__main__':
    args = getArgs()
    mails = gmail.getLastNMails(args.num_mail_read)
    for m in mails:
        print(m)
        print('~'*80)
