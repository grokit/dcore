"""
todo:::a : move in dcore -- it's used as an util lib outside of apps
"""

import math
import json
import datetime
import bisect
import statistics
import os

import dcore.data as data

def bucket(vx, vy, blen, px0 = None):
    """
    Buckets (vx, by) by bucket-length blen.

    Assumes vx, vy already sorted.
    """
    assert len(vx) == len(vy)
    if len(vx) == 0: return vx, vy

    lowvx = vx[0]
    if px0 is not None:
        lowvx = px0
    highvx = vx[len(vx)-1]

    nvx =[lowvx]
    nvy =[0]
    j = 0
    x = lowvx + blen
    while j < len(vy):
        if vx[j] < x:
            nvy[len(nvy)-1] += vy[j]
            j += 1
        else:
            nvx.append(x)
            nvy.append(0)
            x += blen 

    return nvx, nvy


def interpolateWithDamp(vx, vy):
    rangevx = [min(vx), max(vx)]
    step  = 3600 * 24 * 1
    width = 3600 * 24 * 30

    vx_ = []
    vy_ = []
    x = rangevx[0]
    while x <= rangevx[1]:
        i0 = bisect.bisect(vx, x-width)
        i1 = bisect.bisect(vx, x+width)

        store = []
        damps = []
        for i in range(i0, i1):
            dist = abs(vx[i]-x)
            damp = math.e**(-3*dist/width)
            store.append(vy[i]*damp)
            damps.append(damp)

        if len(damps) > 0:
            a = len(damps) / sum(damps)
            store = [v*a for v in store]

            if len(store) > 0:
                y = statistics.mean(store) 
                vx_.append(x)
                vy_.append(y)

        x += step
    return vx_, vy_

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

def plot(vx, vy):
    import numpy as np
    import matplotlib.pyplot as plt

    plt.plot(vx, vy, 'ro', color = '#00b300')

    vx_, vy_ = interpolateWithDamp(vx, vy)
    plt.plot(vx_, vy_, 'k--', color = '#f609ff')

    vxlabels = [unixTimeToDisplay(x) for x in vx]

    lvx = mapToNValues(vx, 6)
    vxlabels = []
    for i in range(len(lvx)):
        j = bisect.bisect(vx, lvx[i]) 
        if j == len(vx): j -= 1
        l = unixTimeToDisplay(vx[j])
        vxlabels.append(l)

    plt.xticks(lvx, vxlabels)
    plt.grid(True)
    plt.show()
