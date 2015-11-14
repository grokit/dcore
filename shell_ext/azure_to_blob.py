"""
# Todo

- Port core to cloud.py where 'save', 'read' and 'del' work as expected.

# Links

- https://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-blob-storage/
- http://azure-storage.readthedocs.org/en
"""

_meta_shell_command = 'cloudwrite'

import os
import argparse
import tempfile
import datetime

from azure.storage.blob import BlobService

containerName = 'scriptsoutput'

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    return args

def listBlobs(blob_service):
    blobs = []
    marker = None
    while True:
        batch = blob_service.list_blobs(containerName, marker=marker)
        blobs.extend(batch)
        if not batch.next_marker:
            break
        marker = batch.next_marker
    return [b.name for b in blobs]

def write(blob_service, name, bytes):
    "http://azure-storage.readthedocs.org/en/latest/blob.html"
    
    blob_service.put_block_blob_from_bytes(
        containerName,
        name,
        bytes)    

def writeFilename(blob_service, name, fullpath):
    rv = blob_service.put_block_blob_from_path(
            containerName,
            name,
            fullpath)    
    print(rv)
    
def autoSetup():
    import dcore.system_description as private_data
    accountName = private_data.azure_personal_account_name
    blob_service = BlobService(account_name=accountName, account_key=private_data.azure_personal_account_key)
    return blob_service
    
def unitTest():
    blob_service = autoSetup()
    
    print(listBlobs(blob_service))
    write(blob_service, 'testFile', ('abc'*int(1e5)).encode())
    writeFilename(blob_service, 'testFile2', r'C:\david\onedrive\backup_scripts_2015-11-10_13-24-44.7z')
    
if __name__ == '__main__':
    
    #unitTest()
    
    args = getArgs()
    simpleDate = str(datetime.datetime.utcnow()).replace(' ', '_')
    writeName = simpleDate + '_' + os.path.split(args.file)[1]
    writeFilename(autoSetup(), writeName, args.file)
    
    