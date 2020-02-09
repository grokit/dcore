import argparse
import hashlib
import binascii
import getpass
import base64

import dcore.private_data as private_data

_meta_shell_command = 'twister'


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--secret',
        default=None,
        help=
        'Value to hash (if do not want to enter in prompt). Careful as this will show in your bash history.'
    )
    parser.add_argument(
        '-f',
        '--file',
        default=None,
        help=
        'Filename to get secret from. Will only get first line and remove endline characters.'
    )
    args = parser.parse_args()
    return args


def __hash20160417(v):
    """
    v: value to `twist`.
    return: twisted value as hex-string representation of binary result.
    """

    scriptSalt = '7vuv4a$yj"vTm)u4omdk^f0rk5\sd9(MiGe7o$cfsym>JLpb%bBgwk7@i6L/ogri2*rcj8h77-j00z;61k75xew'
    secretSalt = private_data.k_lsk_scripts_plaintext_05
    salt = "%s-%s" % (scriptSalt, secretSalt)

    dk = hashlib.pbkdf2_hmac('sha256', v.encode(), salt.encode(), 1000000)
    return binascii.hexlify(dk).decode()


def __fileToSecret(filename):
    with open(filename, 'rb') as fh:
        return base64.b64encode(fh.read()).decode()


# Just point to latest hash function. ALWAYS keep past hash functions in case need to recover an old key.
hash = __hash20160417


def fileTwister(filename):
    return twister(__fileToSecret(filename))


def twister(secret):
    return hash(secret)


if __name__ == '__main__':
    args = getArgs()

    if args.secret is not None:
        secret = args.secret
    elif args.file is not None:
        secret = __fileToSecret(args.file)
    else:
        secret = getpass.getpass(prompt='Enter secret:\n')

    print(twister(secret))
