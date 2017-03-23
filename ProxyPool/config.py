#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
ProxyPool config
'''

import redis

# some config
PROXY_SIZE = 2000
check_IP_URL = 'http://lwons.com/wx'
Check_Spacing_Time = 600

# redis config
REDIS_DATABASE_NAME = 0
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE_NAME)