#!/usr/bin/python3
"""
# Overview

Prove that a note was taken at or before time_x, without having to pre-emptively share all the content of all notes.

# Links

- https://en.wikipedia.org/wiki/Trusted_timestamping

# Example Output

{
    "proof": "0b0ce9103fcf63647285fb45ced452504cf06783956b80c9bedc8306edc44417",
    "hashes": [
        "1c4349fcf429b5653d090fcb05c49d025073ea936a3f4552ddc0b961a0a616a0",
        "8ad5e4be525e23d7237c485530c5af7efd9e5383aabece8f421476d85d078e90"
    ],
    "unixTimeMS": 1497126891443
}
"""

_meta_shell_command = 'sign_notes'

import os
import argparse
import json
import hashlib
import binascii
import time

class SignData:

    def __init__(self):
        self.hashes = []
        self.unixTimeMS = None
        self.proof = None

    def toJSONComplete(self):
        return json.dumps({'proof': self.proof, 'unixTimeMS': self.unixTimeMS, 'hashes': self.hashes}, indent=4)

def getArgs():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

def getAllFiles(rootdir = '.'):
    F = []
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for f in filenames:
            F.append(os.path.normpath(os.path.join(dirpath, f)))
    return F

def _hash(bytesToSign):
    """
    https://docs.python.org/3.6/library/hashlib.html

    Use once Python 3.6 is mainstream:
    BLAKE2 is a cryptographic hash function defined in RFC-7693.
    h = hashlib.blake2b(key=key, digest_size=64)
    h.update(bytesToSign)
    """
    assert type(bytesToSign) == bytes

    key = b'3z/TuQo>zdAMu9SfNd9fcd!HVURJ"FdbdBFOtmY-OnmVO<GGxJO(IhoXA17XPIkY'
    h = hashlib.pbkdf2_hmac('sha256', key, bytesToSign, 10000)
    return binascii.hexlify(h).decode()

def sign(root):
    unixTimeMS = int(time.time()*1000)
    signData = SignData()
    for f in getAllFiles(root):
        with open(f, 'rb') as fh:
            data = fh.read()
        signData.hashes.append(_hash(str(unixTimeMS).encode() + b'_' + data))
    signData.unixTimeMS = unixTimeMS
    allHashs = "".join(signData.hashes).encode()
    signData.proof = _hash(allHashs)
    return signData

if __name__ == '__main__':
    signData = sign('.')
    print(signData.toJSONComplete())

