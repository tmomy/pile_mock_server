#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/5 16:08
"""

class Code(object):
    def __init__(self, code, msg, err_code=0):
        self.code = code
        self.msg = msg
        self.err_code = err_code