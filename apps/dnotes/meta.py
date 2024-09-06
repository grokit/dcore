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
        assert isinstance(meta_type, str)
        assert isinstance(value, str)
        assert isinstance(source_line, str)
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
    return extract_v2(orig_filename, content)


def walk_str(ss, ii, di):
    acc = []
    while ii >= 0 and ii < len(ss):
        if ss[ii] in set('\n\r\t ,'):
            break
        acc.append(ss[ii])
        ii += di
    if di < 0:
        acc.reverse()
    return "".join(acc)


def extract_v2(orig_filename, content):
    assert isinstance(content, str)
    # list of Meta(...) objects.
    metas = []

    lines = content.splitlines()

    for line in lines:
        ii = 0
        buf = line
        while ii != -1:
            ii = buf.find(options.MSEP)
            pre = walk_str(buf, ii - 1, -1)
            post = walk_str(buf, ii + len(options.MSEP), 1)
            if len(pre) > 0 and len(post) > 0:
                metas.append(Meta(pre, post, line, orig_filename))
            buf = buf[ii + len(options.MSEP) + len(post):]

    return metas


def metaToDict(metaList):
    M = {}
    for m in metaList:
        if m.meta_type not in M:
            M[m.meta_type] = set()

        M[m.meta_type].add(m.value)
    return M
