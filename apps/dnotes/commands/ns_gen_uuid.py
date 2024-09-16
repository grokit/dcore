"""
Gen UUIDs.

Note: I believe this is used by my vim plugin as a shell command.
"""

import dcore.apps.dnotes.options as options

import random
import string
import argparse

_meta_shell_command = 'ns_gen_uuid'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--with_prefix', action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    uuid_len = 12
    # note: string.ascii_letters also contains uppercase
    uuid = ''.join(random.choice(string.ascii_lowercase + string.digits) for cc in range(uuid_len))
    prefix = ''
    if get_args().with_prefix:
        prefix = f'uuid{options.MSEP}'
    print(f'{prefix}{uuid}')

