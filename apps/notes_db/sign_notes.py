#!/usr/bin/python3
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
    h = hashlib.blake2b(key=b'3z/TuQo>zdAMu9SfNd9fcd!HVURJ"FdbdBFOtmY-OnmVO<GGxJO(IhoXA17XPIkY', digest_size=64)
    h.update(bytesToSign)
    """
    assert type(bytesToSign) == bytes

    h = hashlib.pbkdf2_hmac('sha256', b'3z/TuQo>zdAMu9SfNd9fcd!HVURJ"FdbdBFOtmY-', b'OnmVO<GGxJO(IhoXA17XPIkY', 100000)
    return binascii.hexlify(h).decode()

def sign(root):
    F = getAllFiles(root)

    unixTimeMS = int(time.time()*1000)
    signData = SignData()
    for f in F:
        with open(f, 'rb') as fh:
            data = fh.read()
        signData.hashes.append(_hash(str(unixTimeMS).encode() + b'_' + data))
    signData.unixTimeMS = unixTimeMS
    allHashs = "".join(signData.hashes).encode()
    signData.proof = _hash(allHashs)
    return signData

if __name__ == '__main__':
    signData = sign('./test_sign')
    print(signData.toJSONComplete())

