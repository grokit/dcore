
import unittest
import os 

import dcore.apps.dnotes.search as search
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.data as data

class Tests(unittest.TestCase):

    def test_folder_override(self):
        data.UNIT_TESTS_OVERRIDE_ROOT_FOLDER = data.test_hijack_root_folder()

        files = util.get_all_note_files()
        for file in files:
            assert '/mock_notes_dir' in file

    def test_search_unique_query(self):
        data.UNIT_TESTS_OVERRIDE_ROOT_FOLDER = data.test_hijack_root_folder()

        files = util.get_all_note_files()
        query = '1892371829371892371982379128309123812930'
        matches = search.extractMatchSetsFromFiles(files, query)
        
        self.assertEqual(len(matches), 1)

        filename = matches[0].filename
        filename = filename[len(data.test_hijack_root_folder()):]
        self.assertEqual(filename, "/low/2021-02-15_16-11_test-note/note.md")


if __name__ == '__main__':
    unittest.main()
