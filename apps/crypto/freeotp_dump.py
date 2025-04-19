"""
Dump the secrets from a freeotp .json export file to the format which is taken by most OTP apps.
"""

import argparse
import json
import base64
import os


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--gen_codes', action='store_true', help='Generate totp codes, requires pyotp installed.')
    args = parser.parse_args()
    return args

def secret_to_char(secret_array):
    ba = b''
    for cc in secret_array:
        ba += cc.to_bytes(1, byteorder='big', signed=True)
    return base64.b32encode(ba)

def gen_totp(secret):
    # keep import here to not require dependency if not generating codes
    import pyotp
    return pyotp.TOTP(secret).now()

if __name__ == '__main__':
    args = get_args()
    filename = args.filename

    with open(filename, 'r') as fh:
        jdata = json.load(fh)

    ids = []
    for tt in jdata['tokenOrder']:
        if ':' in tt:
            tt = tt.split(':')[0]
        ids.append(tt)

    for ii, tt in enumerate(jdata['tokens']):
        who = ids[ii]
        secret =  secret_to_char(tt['secret']).decode()
        totp = ''
        if args.gen_codes:
            totp = gen_totp(secret)
        print(f'{who:<30}: {secret:<40} | {totp}')

