
_meta_shell_command = 'random'

import sys
import argparse
import os

vocab = 'abcdefghijklmnopqrstuvwxyz1234567890'

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, default = 32, nargs='?')
    args = parser.parse_args()
    
    n = args.n
    
    R = []
    while(len(R) < n):
        b = ord(os.urandom(1))
        if b < len(vocab):
            R.append(vocab[b])
    
    print("".join(R))
    