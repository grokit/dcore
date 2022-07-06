"""
This meta class has became the de-facto parser of filename -> metadata.
"""

import re

import dcore.apps.dnotes.options as options


class Meta:
    """
    This is one chunk of metadata.
    """
    def __init__(self, meta_type, value, source_line, source_file):
        """
        Example:

        tag:::tag1
        meta_type: tag
        value: tag1

        tag:::tag1, tag2

        This gets broken into TWO Meta objects.
        """
        assert type(meta_type) == str
        assert type(value) == str
        assert type(source_line) == str
        assert len(source_line.splitlines()) == 1

        self.meta_type = meta_type
        self.value = value
        self.source_line = source_line
        self.source_filename = source_file


    def __str__(self):
        return str("%s: %s" % (self.meta_type, self.value))

    def __repr__(self):
        return self.__str__()


def extract(orig_filename, content):
    """
    content -> T where T is a set of Meta.

    This is an extremely naive parser, might want to enventually replace when I have more than 5 minutes to code.
    Biggest flaw: can only have 1 meta per line.
    """

    assert type(content) == str
    M = []

    lines = content.splitlines()

    for line in lines:
        if re.search('\w%s\w' % options.MSEP, line) is not None:
            LR = line.split(options.MSEP)
            if len(LR) == 0:
                continue
            if len(LR) > 2:
                raise Exception(
                    'Naive parser does not support two tags in one line. Line: %s.'
                    % line)
            l, r = LR

            if ' ' in l:
                l = l.split(' ')[-1]

            R = []
            if ',' in r:
                R = r.split(',')
                R = [r.strip() for r in R]
                if ' ' in R[-1]:
                    R[-1] = R[-1].split(' ')[0]
            else:
                if ' ' in r:
                    r = r.split(' ')[0]
                R.append(r)

            R = [r.strip() for r in R]

            for r in R:
                M.append(Meta(l, r, line, orig_filename))
    return M


def metaToDict(metaList):
    M = {}
    for m in metaList:
        if m.meta_type not in M:
            M[m.meta_type] = set()

        M[m.meta_type].add(m.value)
    return M


