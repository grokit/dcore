"""
# Todo

- Port core to cloud.py where 'save', 'read' and 'del' work as expected.
"""

_meta_shell_command = 'cloudwrite'

import os
import argparse
import tempfile
import datetime

import dcore.iocloud as iocloud

containerName = 'scriptsoutput'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = getArgs()
    simpleDate = str(datetime.datetime.utcnow()).replace(' ', '_')
    writeName = simpleDate + '_' + os.path.split(args.file)[1]

    cloud = iocloud.default()
    cloud.writeFilename(writeName, args.file)
    
