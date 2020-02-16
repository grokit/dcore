"""
Where is the data and strcuture.
"""

import os


def notesRoot():
    dataLocation = os.path.expanduser('~/dnotes')
    try:
        # If you are using dcore system, take root from there.
        import dcore.data as data
        dataLocation = data.dcoreData()
        dataLocation = os.path.join(dataLocation, 'dnotes')
    except ImportError as e:
        pass

    #If want to test...
    #dataLocation = os.path.expanduser('~/Downloads/dnotes')
    return dataLocation


def ingestFilename(root=None):
    if root == None:
        root = notesRoot()
    return os.path.join(root, 'notes/ingest.md')
