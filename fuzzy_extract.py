"""
Fuzzy extract valid files and folders.
"""

import os


def __rm_color(line):
    # remove color marking if present
    # see https://stackoverflow.com/questions/39473297/how-do-i-print-colored-output-with-python-3
    if line[0:2] == '\033[':
        line = line[2:]
        i = line.find('m')
        if i != -1: 
            line = line[i+1:]
            i = line.find('\033[')
            if i != -1: 
                line = line[:i]
    return line

def __rm_colon(line):
    if ':' in line:
        line = line.split(':')[0]
    return line

################################################################################
# PUBLIC API
################################################################################

def extract_files_fuzzy(data, is_file_fn = None):
    if is_file_fn is None:
        is_file_fn = os.path.isfile

    lines = data.splitlines()

    files = set()
    for line in lines:
        line = line.strip()
        line = __rm_color(line)
        if False:
            line = __rm_colon(line)

        if is_file_fn(line):
            files.add(line)

        for chunk in line.split(' '):
            if is_file_fn(chunk):
                files.add(chunk)

    return files

################################################################################
# TEST
################################################################################

__TEST_DATA = """

# Simple

/a/file

# Prefix and suffix

 /b/file
prefix /c/file
/d/file suffix
prefix /e/file suffix
a b cd e f gh 8237@*&@ /f/file js0293)@jSk 

# Subtle: if has spaces, only detect file if line.strip() as a whole 
# contains the file.

/g/file with space
 /h/file with space   

prefix /z/file with space
"""

def __ut_is_file(ss):
    if len(ss) < 2: return False
    # /./file is accepted
    return ss[0] == '/' and ss[2:7] == '/file'

def _unit_test():
    data = __TEST_DATA
    files = extract_files_fuzzy(data, is_file_fn=__ut_is_file)

    expect_out = set([
        '/a/file',
        '/b/file',
        '/c/file',
        '/d/file',
        '/d/file suffix',
        '/e/file',
        '/f/file',
        '/g/file',
        '/g/file with space',
        '/h/file with space',
        '/z/file',
        ])
    print(expect_out.difference(files))
    assert(expect_out.difference(files) == set())

if __name__ == '__main__':
    _unit_test()
