#!/usr/bin/env python
# encoding: utf-8
"""
@author: Tmomy
@time: 2018/1/3 15:22
"""
import os
project_name = ""

redis_pool_configs = {
        "host": "10.10.51.30",
        "port": 6379,
        "pool_size": 5,  # 0表示不使用连接池 最大连接数
        "user_name": "",
        "password": "",
        "db_name": "charge"
}

# 日志配置
log = {
    "name": "pile_mock",
    "level": "debug",
    "console": True,
    "format": "%(thread)d:%(asctime)s %(funcName)s:%(lineno)d %(filename)s - %(name)s %(levelname)s - %(message)s",
    "file": {
        "enable": False,
        "path": ""
    },
    "syslog": {
        "enable": False,
        "ip": "127.0.0.1",
        "port": 10514,
        "facility": "local6"
    },
    "gelf": {
        "enable": True,
        "ip": "10.10.0.63",
        "port": 12201,
        "debug": True,
        "tag": project_name
    }

}