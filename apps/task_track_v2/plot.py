
import math
import json
import datetime
import bisect
import statistics

def interpolateWithDamp(X, Y):
    rangeX = [min(X), max(X)]
    step  = 3600 * 24 * 1
    width = 3600 * 24 * 30

    X_ = []
    Y_ = []
    x = rangeX[0]
    while x <= rangeX[1]:
        i0 = bisect.bisect(X, x-width)
        i1 = bisect.bisect(X, x+width)

        store = []
        damps = []
        for i in range(i0, i1):
            dist = abs(X[i]-x)
            damp = math.e**(-3*dist/width)
            store.append(Y[i]*damp)
            damps.append(damp)

        a = len(damps) / sum(damps)
        store = [v*a for v in store]

        if len(store) > 0:
            y = statistics.mean(store) 
            X_.append(x)
            Y_.append(y)

        x += step
    return X_, Y_

def dateStrToDateTime(d):
    assert d[-3] == ':'
    d = d[0:-3] + d[-2:]
    dt = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%f%z")
    return dt

def dateTimeToUnixTimeSecs(dt):
        return float(dt.strftime("%s"))

def unixTimeToDisplay(unixtime):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.isoformat().split('T')[0]

def mapToNValues(A, n):
    """
    Create an equaly spaced range in min(A), max(A), with n equally spaced values.
    """
    A_ = []
    mn = min(A)
    mx = max(A)
    step = (mx-mn)/(n-1)

    for i in range(n):
        A_.append(mn + step*i)
    assert len(A_) == n
    assert mx == A_[len(A_)-1]
    return A_

def plot(X, Y):
    import numpy as np
    import matplotlib.pyplot as plt

    plt.plot(X, Y, 'ro', color = '#00b300')

    X_, Y_ = interpolateWithDamp(X, Y)
    plt.plot(X_, Y_, 'k--', color = '#f609ff')

    Xlabels = [unixTimeToDisplay(x) for x in X]

    lX = mapToNValues(X, 6)
    Xlabels = []
    for i in range(len(lX)):
        j = bisect.bisect(X, lX[i]) 
        if j == len(X): j -= 1
        l = unixTimeToDisplay(X[j])
        Xlabels.append(l)

    plt.xticks(lX, Xlabels)

    plt.show()

if __name__ == '__main__':
    jd = open('work_tracking_db.json').read()
    jd = json.loads(jd)

    X = []
    Y = []
    for v in jd:
        if v['type'] == 'weight':
            date = v['date']
            unix = dateTimeToUnixTimeSecs(dateStrToDateTime(date))
            if unix < 1485275901: 
                continue

            weight = v['length']
            m = ''
            if weight <= 188: 
                s = math.floor(10*(188-weight))
                m = '<' + '-' * s 
            print(date, weight, m)
            X.append(unix)
            Y.append(weight)
    plot(X, Y)

