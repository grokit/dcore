"""
This meta class has became the de-facto parser of filename -> metadata.
"""

import re
import string

import dcore.apps.dnotes.options as options

##########################################################################
# PRIVATE
##########################################################################

# _REQUIRED_FOR_EXTENDED_META_KVP = '(),=.'


def _walk_str(ss, ii, di):
    return _walk_str_v3(ss, ii, di)


def _walk_str_v3(ss, ii, di):
    """
    di: direction
    """
    acc = []
    while ii >= 0 and ii < len(ss):
        if not (
            ss[ii] in set(
                string.ascii_lowercase +
                string.ascii_uppercase +
                string.digits +
                '-_:')):
            break
        acc.append(ss[ii])
        ii += di
    if di < 0:
        acc.reverse()
    return "".join(acc)


def _match_paren(ss, ii):
    """
    return post from preSEPpost, e.g.: preSEP(k1=v1,...) -> (k1=v1,...)
    """
    assert ss[ii] == '('

    # first implementation: just naive find the next '(' ... asssume '(' is
    # not otherwise permitted
    buf = ss[ii:]
    jj = buf.find(')')
    if jj == -1:
        print('!!!', ss, ii, jj)
        assert jj != -1
    return buf[0:jj + 1]


def _extract_v3(orig_filename, content):
    assert isinstance(orig_filename, str)
    assert isinstance(content, str)

    # list of Meta(...) objects.
    metas = []

    lines = content.splitlines()
    line_no = 0
    for line in lines:
        ii = 0
        buf = line
        while ii != -1:
            ii = buf.find(options.MSEP)
            if ii == -1: break
            pre = _walk_str(buf, ii - 1, -1)
            pos_next_i = ii + len(options.MSEP)

            if pos_next_i + 1 < len(buf) and buf[pos_next_i] == '(':
                # we parse a kvp meta, e.g. preSEP(key1=val1,key2=val2,...)
                post = _match_paren(buf, pos_next_i)
            else:
                # we parse a normal, non-kvp meta, e.g. preSEPpost
                post = _walk_str(buf, pos_next_i, 1)
            if len(pre) > 0 and len(post) > 0:
                metas.append(Meta(pre, post, line, orig_filename, line_no))
            buf = buf[ii + len(options.MSEP) + len(post):]
        line_no += 1

    return metas


def _metaToDict(metaList):
    MM = {}
    for m in metaList:
        if m.meta_type not in MM:
            MM[m.meta_type] = set()
        MM[m.meta_type].add(m.value)
    return MM

##########################################################################
# PUBLIC
##########################################################################


class Meta:
    """
    This is one chunk of metadata.
    """

    def __init__(self, meta_type, value, source_line, source_file, line_no):
        """
        See unit-tests in luid:::u1r1bum7opih for expectations.
        """
        assert isinstance(meta_type, str)
        assert isinstance(value, str)
        assert isinstance(source_line, str)
        assert len(source_line.splitlines()) == 1

        self.meta_type = meta_type
        # note: this can be kvp, but leave that to an outside extension that can
        # interpret the value (keep things orthogonal)
        self.value = value
        self.source_line = source_line
        self.source_filename = source_file
        assert type(line_no) == int
        self.line_no = line_no

    def __str__(self):
        return str("%s: %s" % (self.meta_type, self.value))

    def __repr__(self):
        return self.__str__()


def extract(orig_filename, content):
    return _extract_v3(orig_filename, content)
