#!/usr/bin/env python

"""
utils.py

Utilities that don't really belong anywhere else.
"""

import time


def timed(task):
    """A decorator used for timing function calls."""
    def _decorated(fn):
        def _fn(*args, **kwargs):
            print('[o] %s has begun.' % task)
            start_time = time.time()
            result = fn(*args, **kwargs)
            print('[o] %s has ended (%.4fs elapsed).' % (task, time.time() - start_time))
            return result
        return _fn
    return _decorated


def merge_dicts(*args):
    """Merge an arbitrary number of dictionaries into one."""
    z = args[0].copy()  # start with the first dictionary's keys and values
    for y in args[1:]:
        z.update(y)  # modifies z with y's keys and values & returns None
    return z
