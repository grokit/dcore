"""
Data location.
"""

import os


def get_notes_root_folder():
    dataLocation = os.path.expanduser('~/dnotes')
    try:
        # If you are using dcore system, take root from there.
        import dcore.data as data
        dataLocation = data.dcoreData()
        dataLocation = os.path.join(dataLocation, 'notes')
    except ImportError as e:
        pass

    if False:
        #If want to test...
        #print('hijack dataLocation from: ' + dataLocation)
        dataLocation = os.path.expanduser('~/Downloads/dnotes')
        #print('... to: ' + dataLocation)

    return dataLocation

def get_notes_low_folder():
    return os.path.join(get_notes_root_folder(), 'low')

def get_notes_project_folder():
    return os.path.join(get_notes_root_folder(), 'projects')

def get_notes_articles_folder():
    return os.path.join(get_notes_root_folder(), 'articles')

def get_notes_archive_folder():
    return os.path.join(get_notes_root_folder(), 'archived')

def get_ingest_fullpath():
    return os.path.join(get_notes_root_folder(), 'ingest.md')
