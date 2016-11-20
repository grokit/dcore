"""
# TODO
- Add a compose mode where you can just type text of paste from clipboard until reach EOS character.
- Just use TLS, forbid un-encrypted connection. VERIFY!
"""

import argparse
import time
import base64
import sys

import dcore.private_data as private_data
import dcore.apps.gmail.gmail as gmail

_meta_shell_command = 'reminder'

def getArgs():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('subject', default = ['NONE'], nargs='*')
    parser.add_argument('-t', '--to', default= private_data.primary_email)
    parser.add_argument('-f', '--attachment_filename')
    parser.add_argument('-w', '--work_email', action='store_true', default=False, help='Send to work e-mail instead of default one.')
    
    args = parser.parse_args()
    return args

def attachToBody(toAttachFilename, originBody):
    abytes = open(toAttachFilename, 'rb').read()
    return originBody + "\n\n ** Attachment: %s ** \n\n%s\n\n" % (toAttachFilename, base64.b64encode(abytes))

def argsToStr(args):
    return " ".join(args)

def fromStdInIfData():
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None

TEMPLATE = """
Reminder: %s.

%s

app tag: sq1m9oj9c5oirkqvjz4lug90f0dl52ac.
"""

def decorum(subject, body):
    return TEMPLATE % (subject, body)
    
if __name__ == '__main__':
    
    args = getArgs()

    sin = fromStdInIfData()
    subject = argsToStr(args.subject)
    if sin is None:
        body = ""
    else:
        body = sin

    if args.attachment_filename is not None:
        body += attachToBody(args.attachment_filename, body)

    if args.work_email:
        args.to = private_data.email_work 

    body = decorum(subject, body)
    gmail.do(args.to, subject, body)
