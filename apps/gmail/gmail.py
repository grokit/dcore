"""
Send e-mail from GMail address using username and password stored in a local file.

Tip: don't use an e-mail address you care about, use a non-important e-mail address to send to your real e-mail
     and assume that any data sent can be read by a 3rd party.
"""

import smtplib
import imaplib
import time
import argparse
import dcore.private_data as private_data

def __getCredentials():
    # Get password from pre-install private files.
    gmail_user=private_data.low_security_email
    gmail_pwd=private_data.low_security_email_pw
    return gmail_user, gmail_pwd

def __connect():
    gmail_user, gmail_pwd = __getCredentials()
    server = smtplib.SMTP("smtp.gmail.com", 587)

    # https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.sendmail
    # Put the SMTP connection in TLS (Transport Layer Security) mode. All SMTP commands that follow will be encrypted.
    # Use `sudo tcpdump -Ai wlp1s0 'port 587'` to see the bits on wire, post handshake everything is encrypted.
    server.starttls()

    server.ehlo()
    server.login(gmail_user, gmail_pwd)
    return server, gmail_user

def sendEmail(to, subject, body):

    if isinstance(to, type('')):
        to = [to]

    if isinstance(subject, type([])):
        subject = " ".join(subject)

    success = False
    try:
        server, gmail_user = __connect()
        # From, To, Subject are part of protocol, will show up as mail subject, etc.
        message = "\From: %s\nTo: %s\nSubject: %s\n\n%s" % (gmail_user, ", ".join(to), subject, body) 
        server.sendmail(gmail_user, to, message)
        server.close()
        success = True
    except Exception as e:
        print("Mail sent failed. Exception: %s." % e)

    if success:
        print('Mail sent.')

def getLastNMails(N):

    rawEMails = []
    try:
        # Adapted from:
        # - http://stackoverflow.com/questions/348392/receive-and-send-emails-in-python
        # - https://docs.python.org/3/library/imaplib.html
        username, pw = __getCredentials()

        #  If port is omitted, the standard IMAP4-over-SSL port (993) is used.
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(username, pw)

        # To see which boxes are available.
        if True:
            boxes = mail.list()
            for b in boxes:
                print(b)

        # Somehow this does not work. Would have to look deeper on how to get sent mails.
        #mail.select("[Gmail]/Sent Mail")
        
        mail.select("inbox")

        result, data = mail.search(None, "ALL")
        ids = data[0].split() 

        N = min(N, len(ids))
        for i in range(N):
            result, data = mail.fetch(ids[-(i+1)], "(RFC822)") 
            rawEMails.append(data[0][1])

        mail.close()
    except Exception as e:
        print("Exception: %s." % e)
        return

    M = []
    for m in rawEMails:
        if isinstance(m, type(u'.')):
            m = m.encode('ascii', 'replace')
        m = m.decode()
        M.append(m)
    return M

if __name__ == '__main__':
    mails = getLastNMails(2)
    for m in mails:
        print('~'*80)
        print(m)
        print('~'*80)
