
import os
import re

def readProblems(file, readProblemChunk):
    with open(file) as fh:
        nProbs = int(fh.readline())
        for i in range(0, nProbs):
            yield readProblemChunk(fh)

def solve(solveFn, readProblemChunk, ffilter = '.*'):
    files = [f for f in os.listdir('.') if f[-3:] == '.in' and re.search(ffilter, f) is not None]

    for file in files:
        print("Processing '%s'." % file)
        i = 1
        S = []
        for p in readProblems(file, readProblemChunk):
            result = solveFn(p)
            sol = "Case #%i: %s\n" % (i, result)
            print(sol.strip())
            i += 1
            S.append( sol )
         
        open(file.replace('.in', '.out'), 'w').write( "".join(S) )

