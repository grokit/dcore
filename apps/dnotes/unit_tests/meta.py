
import unittest

import dcore.apps.dnotes.bookmarks as bookmarks
import dcore.apps.dnotes.util as util
import dcore.apps.dnotes.data as data
import dcore.apps.dnotes.meta as module_meta


class Tests(unittest.TestCase):

    def test_simple_meta(self):
        testDoc = """
        \ntag:::tag4

        something prior. tag:::tag1, tag2

        tag:::tag3 not_tag is not a tag since it is not comma separated

        pre:::post

        (check_tag_in_paren:::works)
        """

        meta = module_meta.extract("fake.filename", testDoc)
        assert len(meta) == 5
        metaDict = module_meta.metaToDict(meta)

        assert len(metaDict['tag']) == 3
        assert 'tag1' in metaDict['tag']
        # we used to allow multiple tags seperated by comma, but never used as a feature
        # it has since been removed from the parser
        # assert 'tag2' in metaDict['tag']
        assert 'tag3' in metaDict['tag']
        assert 'tag4' in metaDict['tag']
        assert 'not_tag' not in metaDict['tag']
        assert len(metaDict['pre']) == 1
        assert 'post' in metaDict['pre']

        assert len(metaDict['check_tag_in_paren']) == 1
        assert 'works' in metaDict['check_tag_in_paren']

    def test_two_tag_per_line(self):
        testDoc = """tag:::tag1 tag:::tag2

:::not_tag
        not_tag:::

        aa:::b aa:::c
        bb:::b,bb:::c
        """

        # with spaces at the end
        testDoc += 'not_tag:::              '

        meta = module_meta.extract("fake.filename", testDoc)
        metaDict = module_meta.metaToDict(meta)
        assert len(metaDict['tag']) == 2
        assert 'tag1' in metaDict['tag']
        assert 'tag2' in metaDict['tag']
        assert len(metaDict['aa']) == 2
        assert 'b' in metaDict['aa']
        assert 'c' in metaDict['aa']
        assert len(metaDict['bb']) == 2
        assert 'b' in metaDict['bb']
        assert 'c' in metaDict['bb']

    def test_time_tags(self):
        testDoc = """
        Time tags have to be parseable -- even though it may make sense to change the format at some point
        to not have to have colon in meta.
        time:::2024-09-21_14:03
        """
        meta = module_meta.extract("fake.filename", testDoc)
        metaDict = module_meta.metaToDict(meta)
        assert len(metaDict['time']) == 1
        assert '2024-09-21_14:03' in metaDict['time']

    @unittest.skip("known fail")
    def test_current_confusion(self):

        testDoc = """
        - [item:::bookmark], discover classical art browse and download high-resolution public domain artworks, https://artvee.com/
        """

        meta = module_meta.extract("fake.filename", testDoc)

        """
        Currently:

        [item: bookmark]
        [item: discover classical art browse and download high-resolution public domain artworks
        [item: https://artvee.com/

        ... I think this is a pretty confusing way to extract meta... rething this
        and whether we should save the full line with a meta tag (including potential
        other metas, as we currently do).
        """
        assert len(meta) == 1


if __name__ == '__main__':
    unittest.main()
