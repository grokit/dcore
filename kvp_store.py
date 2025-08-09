"""
Iterable KVP store. (Iterable: not implemented yet, but possible).

- focus on simplicity rather than performance
    - static functions: OK, but would be better if provided class, and static just use default params
        - this would make it easier for testing
        - can be done later though -- can always update transparently

- unit-tests at luid:::25gqkag5mmcu

- status: EXPERIMENTAL
    - read/write there for fun / transient, but nothing serious -- don't want to have to port data until API is stable

# inspiration

- for API: foundation-DB
    - except for using string instead of bytes for simplicity of app-dev?

# goals

- should remain easy to break-off from kvp_store by providing a few function in the same file
    - NO/low dependencies for the same reason

# todo

- unit-tests
    - load-test: what happens if multiple process try to write/read quickly?

- update to store all in same table?
    - ? maybe easier to maintain / export at the price of a bit messier? / less scalable ?
    - although multiple tables would make it easier to break-off a use-case to non-kvp if need to

# maybe-one-day

- could be nice to support postgres transparently

"""

import string
import os
import sqlite3

import dcore.data as ddata

__ALLOWED_CHARS_KEY = set(string.ascii_lowercase + string.digits + '_/')
__DB_FILE = os.path.join(ddata.dcoreTempData(), 'kvp_store.db')

def __assert_key(key):
    assert type(key) == str
    for kk in key:
        if kk not in __ALLOWED_CHARS_KEY:
            err = f'invalid char: {kk} in key or namespace: {key}'
            raise Exception(err)

def __assert_value(value):
    assert type(value) == str

def __table_name(namespace):
    return f'kvp_store_ns_{namespace}'

def __init_and_return_conn(namespace):
    __assert_key(namespace)
    conn = sqlite3.connect(__DB_FILE)
    table_name = __table_name(namespace)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """)
    return conn

def write(key, value, namespace='default'):
    """
    TODO: return different if replace or didn't exist first
    """
    __assert_key(key)
    __assert_value(value)
    conn = __init_and_return_conn(namespace)
    table_name = __table_name(namespace)
    args = (key, value,)
    cur = conn.execute(f"""
    INSERT INTO {table_name} (key, value)
    VALUES (?, ?)
    ON CONFLICT(key) DO UPDATE SET value = excluded.value;
    """, args)
    conn.commit()
    conn.close()

    assert cur.rowcount == 1
    # we can't currently differentiate replaced vs. didn't exist
    return None

def read(key, namespace='default'):
    """
    Return None if doesn't exist.
    """
    __assert_key(key)
    conn = __init_and_return_conn(namespace)
    table_name = __table_name(namespace)
    args = (key,)
    cur = conn.execute(f"SELECT value FROM {table_name} WHERE key = ?", args)
    rows = cur.fetchall()
    if len(rows) == 0:
        return None
    elif len(rows) > 1:
        raise Exception(f'unexpected n. rows: {len(rows)}')
    assert len(rows[0]) == 1
    return rows[0][0]

def read_range(key_begin, key_end, namespace='default'):
    raise NotImplementedException('read_range')

def delete(key, namespace='default'):
    __assert_key(key)
    __assert_key(namespace)
    table_name = __table_name(namespace)
    conn = __init_and_return_conn(namespace)
    cur = conn.execute(f"DELETE FROM {table_name} WHERE key = ?", (key,))
    conn.commit()
    if cur.rowcount == 0:
        return 0
    assert cur.rowcount == 1
    return 1

if __name__ == '__test__':
    pass
