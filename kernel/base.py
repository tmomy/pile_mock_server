#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2018/1/3 11:08
"""
import datetime
from db.db_api import rdc as redis_server
import json


class PileMate(object):

    def __init__(self, terminal_number, gun_number, pile_type, sender_channel, receiver_channel):
        self.RPIX = "pile_mock_" + str(terminal_number)
        self.sender_channel = sender_channel
        self.receiver_channel = receiver_channel
        self.terminal_number = terminal_number
        self.gun_number = int(gun_number)
        self.pile_type = pile_type
        self.status = 0
        self.status_code = {}
        self.pile_price = ""
        self.gun_status = dict()
        self.gun_real_data = {}
        self.init_status_code()
        self.modify_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def init_status_code(self):
        code = [0, 0, 0]*18
        for gn in range(self.gun_number):
            self.status_code[str(gn+1)] = code
        return True

    def redis_set(self):
        info = self.__dict__
        redis_server.set(self.RPIX,json.dumps(info))
        return



