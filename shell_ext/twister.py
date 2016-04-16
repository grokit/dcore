
import argparse
import hashlib 
import binascii

import dcore.system_description as private_data

_meta_shell_command = 'twister'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('src', nargs='+')
    args = parser.parse_args()
    return args

scriptSalt = '7vuv4a$yjsv7Tm)ubku4q4omodkv^f0dr6rv0kW5zssd1k9g(Mnkifcgpi1easj5v7o$cflsy6m>JLpm3byxbcuBmglw5k7@i6Logri2*rcjc8gh77-j00z;61k75xew'
scriptVersion = 2

def hash(v):
    """
    v: value to `twist`.
    return: twisted value as hex-string representation of binary result.
    """

    secretSalt = private_data.sk0
    salt = "%s-%s-%s" % (scriptSalt, secretSalt, scriptVersion)
    dk = hashlib.pbkdf2_hmac('sha256', v.encode(), salt.encode(), 1000000)
    return binascii.hexlify(dk).decode()

if __name__ == '__main__':
    args = getArgs()
    lkey = " ".join(args.src)
    v = hash(lkey)
    print(v)
