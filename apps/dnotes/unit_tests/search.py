
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

    def test_search_two_words_different_place_in_file(self):
        data.UNIT_TESTS_OVERRIDE_ROOT_FOLDER = data.test_hijack_root_folder()

        files = util.get_all_note_files()

        words = ['test_word_gok2t6ebrxpl', 'test_word_nvmoaw0aboxo']

        query = '' 
        for ww in words:
            query += f' {ww} '
        matches = search.extractMatchSetsFromFiles(files, query)
        
        self.assertEqual(len(matches), 1)

        filename = matches[0].filename
        filename = filename[len(data.test_hijack_root_folder()):]
        self.assertEqual(filename, "/articles/ut_search_different_lines/note.md")

        # this is subtle, and perhaps too fragile for a test. when we do entire file search
        # more than one line match ... we keep the first one
        # the first one is based on (arbitrary) search order: we currently do word-by-word
        # in query starting from first. this is why first word matches, but not second
        self.assertTrue(words[0] in matches[0].line)
        self.assertFalse(words[1] in matches[0].line)

    def test_search_must_match_all_terms(self):
        data.UNIT_TESTS_OVERRIDE_ROOT_FOLDER = data.test_hijack_root_folder()

        files = util.get_all_note_files()

        words = ['test_word_gok2t6ebrxpl', 'test_word_NOT_PRESENT_IN_FILE']

        query = '' 
        for ww in words:
            query += f' {ww} '
        matches = search.extractMatchSetsFromFiles(files, query)
        
        self.assertEqual(len(matches), 0)

if __name__ == '__main__':
    unittest.main()
