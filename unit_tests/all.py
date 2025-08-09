
import unittest
import io

import dcore.unit_tests.kvp_store as kvp_store

def suite():
    """
    https://docs.python.org/3/library/unittest.html
    """
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(kvp_store.Tests))
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


