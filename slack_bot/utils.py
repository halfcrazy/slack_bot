#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool
from functools import wraps


def timeout(g, seconds, default="timeout"):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(fn, args=args, kwds=kwargs)
            try:
                # the time cost before start fn
                cost_time = time.time() - g.time
                return async_result.get(seconds - cost_time)
            except TimeoutError:
                return default() if callable(default) else default
            finally:
                pool.close()
                pool.terminate()
        return wrapper
    return decorator
