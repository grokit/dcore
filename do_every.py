
import os
import json
import time
import hashlib

import dcore.data as data
import dcore.dlogging as dlogging

def _hash(filename):
    with open(filename, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def isFileModifiedSinceLastTouch(filename):
    cache = os.path.join(data.dcoreTempData(), 'file_hash_cache.json')

    # If no information on file, has never been touched.
    if not os.path.isfile(cache):
        return True

    fhash = _hash(filename)
    with open(cache, 'r') as fh:
        hashMap = json.loads(fh.read())
        if filename in hashMap:
            if hashMap[filename] == fhash:
                return False

    return True

def markFileAsCurrent(filename):
    cache = os.path.join(data.dcoreTempData(), 'file_hash_cache.json')

    hashMap = {}
    if os.path.isfile(cache):
        with open(cache, 'r') as fh:
            hashMap = json.loads(fh.read())

    filename = os.path.abspath(filename)
    hashMap[filename] = _hash(filename) 

    with open(cache, 'w') as fh:
        fh.write(json.dumps(hashMap, sort_keys=True, indent=4))

    assert not isFileModifiedSinceLastTouch(filename)

def _lastTimeDone(key):
    filename = os.path.join(data.dcoreTempData(), 'do_every.json')

    if not os.path.isfile(filename):
        return 1e9

    with open(filename, 'r') as fh:
        keys = json.loads(fh.read())
        if not key in keys:
            return 1e9
        utime = keys[key]

        now = int(time.time())

        nHoursAgo = (now - utime) / (60*60)
        return nHoursAgo

def _markDone(key):
    filename = os.path.join(data.dcoreTempData(), 'do_every.json')

    if not os.path.isfile(filename):
        with open(filename, 'w') as fh:
            fh.write(json.dumps({}))

    keys = {}
    if os.path.isfile:
        with open(filename, 'r') as fh:
            keys = json.loads(fh.read())

    # unixtime
    keys[key] = int(time.time())

    with open(filename, 'w') as fh:
        fh.write(json.dumps(keys, sort_keys=True, indent=4))

    assert _isDoneInLastXHours(key, 0.01)

def _isDoneInLastXHours(key, nHours):
    return _lastTimeDone(key) <= nHours

def doEvery(key, nHours, fn, log=True):
    if not _isDoneInLastXHours(key, nHours):
        fn()
        _markDone(key)
    else:
        if log:
            dlogging.logging.debug('Skipping %s, it was done %.2f hour(s) ago (doing every %.2f hour(s)).', key, _lastTimeDone(key), nHours)

if __name__ == '__main__':
    key = 'test-key_%s' % int(time.time())
    assert _isDoneInLastXHours(key, 1) is False
    _markDone(key)
    assert _isDoneInLastXHours(key, 1) is True
    assert _isDoneInLastXHours(key, 0.5) is True
    assert _isDoneInLastXHours(key, 0.1) is True
    assert _isDoneInLastXHours(key, 0.0013889) is True

    time.sleep(6)

    assert _isDoneInLastXHours(key, 0.0013889) is False


