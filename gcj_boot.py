
import os
import re
import time 

def readProblems(file, readProblemChunk):
    with open(file) as fh:
        nProbs = int(fh.readline())
        for i in range(0, nProbs):
            yield readProblemChunk(fh)

def solve(solveFn, readProblemChunk, ffilter = '.*'):
    files = [f for f in os.listdir('.') if f[-3:] == '.in' and re.search(ffilter, f) is not None]

    fhStats = open('processing.stats', 'a')
    for file in files:
        logLine = "Processing '%s'." % file
        print(logLine)
        fhStats.write("%s [at %s].\n" % (logLine, time.strftime("%Y-%m-%d %H:%M:%S")))
        fhStats.flush()

        fileOut = file.replace('.in', '.out')
        fh = open(fileOut, 'w')

        S = []
        for i, p in enumerate(readProblems(file, readProblemChunk)):
            result = solveFn(p)
            sol = "Case #%i: %s\n" % (i+1, result)
            print(sol.strip('\n'))
            fh.write(sol)
            fh.flush()
            fhStats.write("%s [at %s].\n" % (sol, time.strftime("%Y-%m-%d %H:%M:%S")))
            fhStats.flush()
        fh.close()

        fhStats.write('Done at %s.\n' % time.strftime("%Y-%m-%d %H:%m:%S"))
        fhStats.flush()
