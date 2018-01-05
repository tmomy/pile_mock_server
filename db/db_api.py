#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/3 15:27
"""
from config.conf import redis_pool_configs
from db.redis_servce.redis_conn import engine

rdc = engine(redis_pool_configs)