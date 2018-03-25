
import math
import json
import datetime
import bisect
import statistics
import os

import dcore.data as data

import plot_utils

_meta_shell_command = 'plot_weight'

if __name__ == '__main__':
    folder = data.dcoreData()
    jd = open(os.path.join(folder, 'work_tracking_db.json')).read()
    jd = json.loads(jd)

    X = []
    Y = []
    for v in jd:
        if v['type'] == 'weight':
            date = v['date']
            unix = plot_utils.dateTimeToUnixTimeSecs(plot_utils.dateStrToDateTime(date))
            if unix < 1485275901 + 10 * 60*60*24*30: 
                continue

            weight = v['length']
            m = ''
            if weight <= 188: 
                s = math.floor(10*(188-weight))
                m = '<' + '-' * s 
            print(date, weight, m)
            X.append(unix)
            Y.append(weight)
    plot_utils.plot(X, Y)

