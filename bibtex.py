"""
Tool to parse bibtex files and print references.

This is not meant to give an output which follows strict academic
layout rules, but to just be able to refer from a bibtex file such
that I don't have to keep two separate reference systems (one for 
academia, one for personal notes or blog).

## Format

@type {name,
   key1 = {value1},
   key2 = {value2}
}

"""

_meta_shell_command = 'bib'

import os
import sys

import dcore.data as data


# TODO: when done, move references.bib to dcored, just keep in web json export.

class Reference:

    def __init__(self):
        """
        There are lots of fields, we do not populate all of them.
        """
        author = None
        title = None
        year = None
        url = None
        journal = None

def unit_tests():
    pass

if __name__ == '__main__':
    unit_tests()
