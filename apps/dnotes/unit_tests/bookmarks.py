
import unittest

import dcore.apps.dnotes.bookmarks as bookmarks
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.meta as module_meta

class Tests(unittest.TestCase):

    def test(self):
        data.UNIT_TESTS_OVERRIDE_ROOT_FOLDER = data.test_hijack_root_folder()
        b_marks = bookmarks.get_bookmarks()

        urls = set([bb.url for bb in b_marks])
        self.assertTrue('https://www.rijksmuseum.nl/en' in urls)

        values = set([bb.value for bb in b_marks])
        self.assertTrue('], smart cs person, https://bellard.org/' in values)

if __name__ == '__main__':
    unittest.main()
