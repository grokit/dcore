
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
        fileOut = file.replace('.in', '.out')
        fh = open(fileOut, 'w')

        S = []
        for i, p in enumerate(readProblems(file, readProblemChunk)):
            result = solveFn(p)
            sol = "Case #%i: %s\n" % (i+1, result)
            print(sol.strip('\n'))
            fh.write(sol)
        fh.close()
