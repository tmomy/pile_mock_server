#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2018/1/2 14:11
"""
import time
import gevent
from gevent import monkey
import json
import traceback

from base import PileMate
from db.db_api import rdc as redis_server
from log_servce.logs import sys_logging
monkey.patch_all()


class Pile(PileMate):
    def __init__(self, pd):
        PileMate.__init__(self, pd['tn'], pd['gn'], pd['pty'], pd['sc'], pd['rc'])
        self.timer = 15
        self.LOGIN_RESP = True
        self.STOP_HEART = True
        # 收到消息
        self.func = ''
        self.r_gn = ''
        self.r_msg = {}

        # 充电

        self.redis_set()

    def heartbeat(self):
        while True:
            if not self.LOGIN_RESP:
                self.send_msg(msg={}, msg_type="heartbeat", gn=0)
            gevent.sleep(self.timer)

    def heartbeat_rspn(self):
        success = self.r_msg.get('success')
        if success:
            self.STOP_HEART = False

    def upload_alarm(self):
        data = {
            "events": []
        }
        msg_type = "upload_alarm"
        while True:
            if not self.LOGIN_RESP:
                for gn, code in self.status_code.items():
                    data['events'] = code
                    self.send_msg(msg_type=msg_type, msg=data, gn=gn)
            gevent.sleep(self.timer * 2)

    def upload_alarm_rspn(self):
        success = self.r_msg.get('success')
        if success:
            return True

    def action_control(self):
        gun_status = {
            'serial_number': "",
            'charge_mode': 0,
            'charge_constraint': "",
        }
        pass

    def gun_input(self):
        gn = self.r_msg['gn']
        battery_capacity = self.r_msg['battery_capacity']
        rated_power = self.r_msg['rated_power']
        if gn not in self.status_code.keys():
            return False
        gun_status = {
            'gn': gn
        }
        pass

    def login(self):
        msg_type = "login"
        re_code = 0
        while True:
            if re_code in [0, 3]:
                while self.LOGIN_RESP:
                    self.send_msg(msg={}, msg_type=msg_type,gn=0)
                    gevent.sleep(1)
            if self.STOP_HEART:
                re_code += 1
                if re_code == 3:
                    self.LOGIN_RESP = True
                    re_code = 0
            gevent.sleep(15)

    def login_rspn(self):
        success = self.r_msg.get('success')
        if success:
            self.LOGIN_RESP = False

    def send_msg(self, msg=None, msg_type=None, gn=None):
        if msg is None:
            msg = {
                "success": True
            }
        fun = msg_type
        resp = {
            "terminal_number": self.terminal_number,
            "msg_type": fun,
            "pile_type": int(self.pile_type),
            "gun_number": int(gn),
            "data": msg
        }
        msgs = json.dumps(resp)
        redis_server.publish(self.sender_channel, msgs)
        sys_logging.info("[channel]: {}|[tn]:{}, [msg]:{}".format(self.sender_channel, self.terminal_number, msgs))
        return True

    def listen(self):
        pub_sub = redis_server.pubsub()
        receiver = [self.receiver_channel]
        pub_sub.subscribe(receiver)
        for item in pub_sub.listen():
            str_data = item['data']
            sys_logging.debug("【{}】pile_receiver: {}".format("receiver", json.dumps(str_data)))
            if str_data not in [None, 1]:
                try:
                    data = json.loads(str_data)
                    tn = data['terminal_number']
                    msg_type = data['msg_type']
                    pty = data['pile_type']
                    gn = data['gun_number']
                    msg = data['data']
                    if tn == self.terminal_number and pty == self.pile_type:
                        self.func = msg_type
                        self.r_gn = gn
                        self.r_msg = msg
                        super(Pile, self).__getattribute__(self.func)()
                except:
                    sys_logging.debug("【{}】listen:{}".format("receiver", traceback.format_exc()))
        pass

    def run(self):
        print "start..."
        jobs = list()
        jobs.append(gevent.spawn(self.login))
        jobs.append(gevent.spawn(self.heartbeat))
        jobs.append(gevent.spawn(self.upload_alarm))
        jobs.append(gevent.spawn(self.listen))
        while True:
            time.sleep(5)
            print "running..."
    pass


def a__pile(pds):
    p1 = Pile(pds)
    print json.dumps(p1.__dict__)
    a = redis_server.get("pile_mock_0001")
    p1.run()


if __name__ == '__main__':
    pd = {
        'tn': "000000000011",
        'gn': 2,
        'pty': 1,
        'sc': u"apl_res",
        'rc': u"apl_req"
    }
    a__pile(pd)
