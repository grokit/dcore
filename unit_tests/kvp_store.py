
import unittest
import os
import uuid

import dcore.kvp_store as kvp_store


class Tests(unittest.TestCase):
    """
    uuid:::25gqkag5mmcu
    """

    def test_simple(self):
        random_suffix = str(uuid.uuid1()).replace('-', '_')
        test_key = f'not_exist_{random_suffix}'
        test_val = f'test_val_{random_suffix}'
        rv = kvp_store.read(test_key, namespace='unit_tests')
        if rv is not None:
            raise Exception(f'expect None, got: {rv}')
        kvp_store.write(test_key, test_val, namespace='unit_tests')
        kvp_store.write(test_key, test_val, namespace='unit_tests')

        rv = kvp_store.read(test_key, namespace='unit_tests')
        if rv != test_val:
            err = f'{rv} != {test_val}'
            raise Exception(err)
        rv = kvp_store.delete(test_key, namespace='unit_tests')
        assert (rv == 1)
        rv = kvp_store.read(test_key, namespace='unit_tests')
        assert (rv is None)
        rv = kvp_store.delete(test_key, namespace='unit_tests')
        assert (rv == 0)

    def test_ranges(self):
        """
        Make sure catch exception.
        """
        pass

    def test_export(self):
        """
        TODO: leverage this to keep a text backup of all data?
        """
        pass


if __name__ == '__main__':
    if True:
        unittest.main()
    else:
        # run a specific test ...
        suite = unittest.TestLoader().loadTestsFromName('kvp_store.Tests.test_simple')
        unittest.TextTestRunner().run(suite)
