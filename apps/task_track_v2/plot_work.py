
import math
import json
import datetime
import bisect
import statistics
import os

import dcore.data as data

import plot_utils

_meta_shell_command = 'plot_work'

if __name__ == '__main__':
    folder = data.dcoreData()
    jd = open(os.path.join(folder, 'work_tracking_db.json')).read()
    jd = json.loads(jd)

    X = []
    Y = []
    for v in jd:
        if v['type'] == 'work':
            date = v['date']
            xtime = plot_utils.dateTimeToUnixTimeSecs(plot_utils.dateStrToDateTime(date))
            if xtime < 1485275901: 
                continue

            # Obvious issue: need to add all days where there is 0
            # work done. Bucket and add days with multiple reports.
            nwork = v['length']
            X.append(xtime)
            Y.append(nwork)
    plot_utils.plot(X, Y)

