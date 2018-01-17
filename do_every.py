
import os
import json
import time

import dcore.data as data

def markDone(key):
    pass

def isDoneInLastXHours(key, nhours):
    filename = os.path.join(data.dcoreData(), 'do_every.json')

    if not os.path.isfile(filename):
        return False

    with open(filename, 'r') as fh:
        keys = json.loads(fh.read())
        if not key in keys:
            return False
        utime = keys[key]

        now = int(time.time())

        nHoursAgo = (now - utime) / (60*60)
        return nHoursAgo <= nhours

def markDone(key):
    filename = os.path.join(data.dcoreData(), 'do_every.json')

    with open(filename, 'r') as fh:
        keys = json.loads(fh.read())

    # unixtime
    keys[key] = int(time.time())

    with open(filename, 'w') as fh:
        fh.write(json.dumps(keys))

    assert isDoneInLastXHours(key, 0.01)

if __name__ == '__main__':
    key = 'test-key_%s' % int(time.time())
    assert isDoneInLastXHours(key, 1) is False
    markDone(key)
    assert isDoneInLastXHours(key, 1) is True
    assert isDoneInLastXHours(key, 0.5) is True
    assert isDoneInLastXHours(key, 0.1) is True
    assert isDoneInLastXHours(key, 0.0013889) is True

    time.sleep(5)

    assert isDoneInLastXHours(key, 0.0013889) is False


    

