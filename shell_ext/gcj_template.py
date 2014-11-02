
_meta_shell_command = 'gcjt'

template = """ \"\"\"
This script may use libraries publicly available at: https://github.com/grokit/dcore.

Does this solution solve:
   Small: ?.
   Big:   ?.
\"\"\"

import dcore.gcj_boot as boot

class Problem:
    pass

def readProblem(fh):

    n, m = [int(x) for x in fh.readline().strip().split()]

    problem = Problem()
    return problem

def solve(P):
    return -1

boot.solve(solve, readProblem, '.*tiny')
"""

if __name__ == '__main__':
    open('code.py', 'w').write(template)
