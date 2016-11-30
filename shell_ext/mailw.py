"""
MailW: Mail Write. Send mail using pre-configured (username, pw) on machine.
"""

import argparse
import time
import base64
import sys

import dcore.private_data as private_data
import dcore.apps.gmail.gmail as gmail

_meta_shell_command = 'mailw'

TEMPLATE = """
Reminder: %s.

%s
"""

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

    if args.work_email:
        args.to = private_data.email_work 

    if subject == 'NONE' and args.attachment_filename is not None:
        subject = args.attachment_filename

    body = decorum(subject, body)
    if isinstance(body, type(u'.')):
        body = body.encode('ascii', 'replace')
        body = body.decode()

    msgAsStr = gmail.sendEmail(args.to, subject, body, args.attachment_filename)
    L = msgAsStr.splitlines()
    if len(L) > 30:
        L = L[0:30]
        L += ['[... truncated ...]']
    print("\n".join(L))


