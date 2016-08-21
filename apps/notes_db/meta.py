
import re

class Meta:

    def __init__(self, metaType, value):
        """
        Example:

        tag::tag1
        metaType: tag
        value: tag1

        tag::tag1, tag2

        This gets broken into TWO Meta objects.
        """
        assert type(metaType) == type('')
        assert type(value) == type('')

        self.metaType = metaType
        self.value = value

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

def extract(content):
    "content -> T where T is a set of Meta."
    "This is an extremely naive parser, might want to enventually replace when I have more than 5 minutes to code."
    M = []

    lines = content.splitlines()

    for line in lines:
        if re.search('\w::\w', line) is not None:
            LR = line.split('::')
            if len(LR) == 0:
                continue
            if len(LR) > 2:
                raise Exception('Naive parser does not support two tags in one line. Line: %s.' % line)
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
                M.append(Meta(l, r))
    return M

def metaToDict(metaList):
    M = {}
    for m in metaList:
        if m.metaType not in M:
            M[m.metaType] = set()

        M[m.metaType].add(m.value)
    return M

def unitTest():
    testDoc = """
    \ntag::tag4

    something prior. tag::tag1, tag2

    tag::tag3 not_tag is not a tag since it is not comma separated

    pre::post
    """

    meta = extract(testDoc)
    for m in meta:
        print(m)
    assert len(meta) == 5
    metaDict = metaToDict(meta)

    assert len(metaDict['tag']) == 4
    assert 'tag1' in metaDict['tag']
    assert 'tag2' in metaDict['tag']
    assert 'tag3' in metaDict['tag']
    assert 'tag4' in metaDict['tag']
    assert 'not_tag' not in metaDict['tag']
    assert len(metaDict['pre']) == 1
    assert 'post' in metaDict['pre']

if __name__ == '__main__':
    unitTest()

