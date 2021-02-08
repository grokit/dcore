
import unittest

import dcore.apps.dnotes.unit_tests.bookmarks as ut_bookmarks
import dcore.apps.dnotes.unit_tests.tags as ut_tags
import dcore.apps.dnotes.unit_tests.search as ut_search
import dcore.apps.dnotes.unit_tests.meta as ut_meta

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ut_bookmarks.Tests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ut_tags.Tests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ut_search.Tests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ut_meta.Tests))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())



