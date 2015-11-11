import sys

_meta_shell_command = 'template_gcj'

template = """\"\"\"
This script may use libraries publicly available at: https://github.com/grokit/dcore.

Does this solution solve:
   Small: ?.
   Big:   ?.
\"\"\"

from dcore.cs.gcd import gcd
from dcore.cs.lcm import lcm
from dcore.cs.factorization import primeFactorization as factorization

import dcore.gcj_boot as boot

def readProblem(fh):

    n, m = [int(x) for x in fh.readline().strip().split()]

    return (n, m)

def solve(p):
    return -1

boot.solve(solve, readProblem, '.*tiny')
"""

if __name__ == '__main__':
    name = 'code.py'

    if len(sys.argv) > 1:
        name = sys.argv[1]

    open(name, 'w').write(template)
