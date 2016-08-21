import os

def createFolderIfNotExist(folder):
    if not os.path.isdir(folder):
        print('Folder does not exist, creating.')
        os.makedirs(folder)

def createFileIfNotExist(file):
    if not os.path.isfile(file):
        print('File does not exist, creating.')
        with open(file, 'w') as fh:
            fh.write('')

