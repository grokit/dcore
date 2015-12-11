"""
IOCloud: read and write files to the cloud.

# Setup

sudo apt-get install python3-setuptools
sudo easy_install3 pip
sudo pip3.4 install azure
sudo pip3.4 install azure-storage
?? how to do it for py3?

# Documentation / Links 

- https://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-blob-storage/
- http://azure-storage.readthedocs.org/en

"""

from azure.storage.blob import BlobService

class IOCloudAzure:

    def __init__(self, accountName, accountKey):
        self.containerName = 'default'
        self.handle = BlobService(account_name=accountName, account_key=accountKey)

        # If already exists, will just nop.
        self.handle.create_container(self.containerName)

    def write(self, name, bytess):
        "http://azure-storage.readthedocs.org/en/latest/blob.html"
        
        self.handle.put_block_blob_from_bytes(
            self.containerName,
            name,
            bytess)    

    def writeFilename(self, name, fullpath):
        rv = self.handle.put_block_blob_from_path(
                self.containerName,
                name,
                fullpath)    
        print(rv)

    def listBlobs(self):
        blobs = []
        marker = None
        while True:
            batch = self.handle.list_blobs(self.containerName, marker=marker)
            blobs.extend(batch)
            if not batch.next_marker:
                break
            marker = batch.next_marker
        return [b.name for b in blobs]

def default():
    import dcore.system_description as private_data
    accountName = private_data.azure_personal_account_name
    accountKey = private_data.azure_personal_account_key
    ioCloud = IOCloudAzure(accountName, accountKey)
    return ioCloud
    
def unitTest():
    cloud = default()
    
    print(cloud.listBlobs())
    cloud.write('testBytes', ('abc'*int(1e5)).encode())

    testFile = 'testFile'
    #open(testFile).write('test')
    cloud.writeFilename('testFileBlobName', testFile)

if __name__ == '__main__':
    unitTest()

