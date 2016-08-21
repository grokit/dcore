"""
Send e-mail from GMail address.

# TODO

- Move to sa-utils
"""

import smtplib
import time
import argparse
import dcore.system_description as private_data

_meta_shell_command = 'gmail'

def getArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--to', required=True)
    parser.add_argument('subject', nargs='+')
    parser.add_argument(
        '-b',
        '--body',
        default='This is a test, not spam (%s).' %
        time.strftime('%Y-%m-%d %H:%M %Ss'))

    args = parser.parse_args()
    return args

def send_email(
        to,
        gmail_user=private_data.low_security_email,
        gmail_pwd=private_data.low_security_email_pw,
        subject="subject",
        body="body"):

    print(
        "%s sends to %s, subject: '%s', body='%s'" %
        (gmail_user, to, subject, body))

    if isinstance(to, type('')):
        to = [to]

    if isinstance(subject, type([])):
        subject = " ".join(subject)

    # Prepare actual message
    message = "\From: %s\nTo: %s\nSubject: %s\n\n%s" % (
        gmail_user, ", ".join(to), subject, body)

    success = False
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(gmail_user, to, message)
        server.close()
        success = True
    except Exception as e:
        print("Mail sent failed. Exception: %s." % e)

    if success:
        print('Mail sent.')


def do(to, subject, body):
    send_email(to, body=body, subject=subject)

if __name__ == '__main__':

    args = getArgs()
    print(args)
    do(args.to, args.subject, args.body)
