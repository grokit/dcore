import os
import json
import time
import hashlib

import dcore.data as data

def hash(filename):
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

    fhash = hash(filename)
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
    hashMap[filename] = hash(filename) 

    with open(cache, 'w') as fh:
        fh.write(json.dumps(hashMap))

    assert not isFileModifiedSinceLastTouch(filename)

def isDoneInLastXHours(key, nhours):
    filename = os.path.join(data.dcoreTempData(), 'do_every.json')

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

    time.sleep(6)

    assert isDoneInLastXHours(key, 0.0013889) is False


