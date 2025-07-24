
import unittest
import io

import dcore.apps.dnotes.unit_tests.search as ut_search
import dcore.apps.dnotes.unit_tests.meta as ut_meta

def suite():
    """
    https://docs.python.org/3/library/unittest.html
    """
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ut_search.Tests))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(ut_meta.Tests))
    return suite

def hook_external_validator():
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream)
    return runner.run(suite()), stream.getvalue()

if __name__ == '__main__':
    rv, stream = hook_external_validator()
    print(stream)
    if len(rv.failures) + len(rv.errors) != 0:
        print(stream)
    else:
        print('ALL GOOD')


