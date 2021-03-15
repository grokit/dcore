
import unittest

import dcore.apps.dnotes.bookmarks as bookmarks
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.meta as module_meta

class Tests(unittest.TestCase):

    def test_basic(self):
        data.UNIT_TESTS_OVERRIDE_ROOT_FOLDER = data.test_hijack_root_folder()
        b_marks = bookmarks._extract_bookmarks()

        urls = set([bb.url for bb in b_marks])
        self.assertTrue('https://www.rijksmuseum.nl/en' in urls)

        values = set([bb.value for bb in b_marks])
        # This also checks we remove the funny first characters
        self.assertTrue('smart cs person; library of personal projects, https://bellard.org/' in values)

    def test_query(self):
        data.UNIT_TESTS_OVERRIDE_ROOT_FOLDER = data.test_hijack_root_folder()

        b_marks = bookmarks.get_bookmarks_matching(['library'])
        values = set([bb.value for bb in b_marks])
        assert len(values) == 2
        self.assertTrue('smart cs person; library of personal projects, https://bellard.org/' in values)
        self.assertTrue('ACM digital library, https://dl.acm.org/' in values)

        # more restrictive: two terms, expect to filter down to ACM only
        b_marks = bookmarks.get_bookmarks_matching(['library', 'ACM'])
        values = set([bb.value for bb in b_marks])
        assert len(values) == 1
        self.assertTrue('ACM digital library, https://dl.acm.org/' in values)

    def test_shortlink(self):
        data.UNIT_TESTS_OVERRIDE_ROOT_FOLDER = data.test_hijack_root_folder()

        b_marks = bookmarks.get_bookmarks_matching(['st url shortened'])
        values = set([bb.value for bb in b_marks])
        assert len(values) == 1
        self.assertTrue('test url shortened, short/link/to/web' in values)
        urls = set([bb.url for bb in b_marks])
        assert len(urls) == 1
        self.assertTrue('short/link/to/web' in urls)

if __name__ == '__main__':
    unittest.main()
