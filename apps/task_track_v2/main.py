"""
# TODO
"""

import argparse
import json

def getArgs():

    parser = argparse.ArgumentParser()

    #parser.add_argument('-t', '--to', required=True)
    #parser.add_argument('subject', nargs='+')
    args = parser.parse_args()
    return args

class TaskEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class Test:

    def __init__(self):
        self.a = 1

if __name__ == '__main__':
    args = getArgs()

    t = Test()
    tj = TaskEncoder().encode(t)
    print(tj)
    pass
