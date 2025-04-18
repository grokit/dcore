"""
Data location.
"""

import os

UNIT_TESTS_OVERRIDE_ROOT_FOLDER = None

def test_hijack_root_folder():
    path, _ = os.path.split(__file__)
    return os.path.join(path, 'unit_tests/mock_notes_dir')

def get_notes_root_folder():
    if UNIT_TESTS_OVERRIDE_ROOT_FOLDER is not None:
        return UNIT_TESTS_OVERRIDE_ROOT_FOLDER

    dataLocation = os.path.expanduser('~/dnotes')
    try:
        # If you are using dcore system, take root from there.
        import dcore.data as data
        dataLocation = data.dcoreData()
        dataLocation = os.path.join(dataLocation, 'notes')
    except ImportError as e:
        pass

    return dataLocation

def get_notes_folders_ext():
    if UNIT_TESTS_OVERRIDE_ROOT_FOLDER is not None:
        return []
    out = []
    out.append(os.path.expanduser('~/sync/dev/windows_computer/sync_w_win'))
    out.append(os.path.expanduser('~/low_sync/sync_phone'))
    # note: do not put dcore to avoid accidental leaking / taking notes in a public file
    out.append(os.path.expanduser('~/sync/scripts/dcore_ext'))
    out = [oo for oo in out if os.path.exists(oo) and os.path.isdir(oo)]
    return out

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
