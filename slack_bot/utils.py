#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool
from functools import wraps

from flask import current_app as app


def timeout(seconds=None, default='timeout'):
    if not seconds:
        seconds = app.config.get('TIMEOUT', 25)
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(fn, args=args, kwds=kwargs)
            try:
                return async_result.get(seconds)
            except TimeoutError:
                if callable(default):
                    return default()
                else:
                    return default
        return wrapper
    return decorator
