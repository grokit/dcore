"""
Send e-mail from GMail address.
"""

import smtplib
import time
import argparse
import dcore.private_data as private_data

"""
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
"""

def sendEmail(
        to,
        gmail_user=private_data.low_security_email,
        gmail_pwd=private_data.low_security_email_pw,
        subject="subject",
        body="body"):

    #print( "%s sends to %s, subject: '%s', body='%s'" % (gmail_user, to, subject, body))

    if isinstance(to, type('')):
        to = [to]

    if isinstance(subject, type([])):
        subject = " ".join(subject)

    # From, To, Subject are part of protocol, will show up as mail subject, etc.
    message = "\From: %s\nTo: %s\nSubject: %s\n\n%s" % (gmail_user, ", ".join(to), subject, body) 
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
    sendEmail(to, body=body, subject=subject)

"""
if __name__ == '__main__':

    args = getArgs()
    print(args)
    do(args.to, args.subject, args.body)
"""
