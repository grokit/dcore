import os
import argparse
import time

_meta_shell_command = 'flake'

def allocNowFile():
    base = '/media/75a94e19-dccf-477a-bd80-251f0231a0b1/data/dev/flakes/'
    # os.path.expanduser('~')
    return os.path.join( base, time.strftime('%Y-%m-%d_%H-%M') + '.flake' )

if __name__ == '__main__':
	file = allocNowFile()
	os.system('vim %s' % file)

	


