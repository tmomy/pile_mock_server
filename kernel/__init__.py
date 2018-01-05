#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2018/1/2 10:34
"""
from functools import wraps
from db.db_api import rdc as redis_server
from log_servce.logs import sys_logging


def coroutine(func):
    """装饰器，预激活func"""
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer
