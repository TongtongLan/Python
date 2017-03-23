#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

class service_conn:
    @staticmethod
    def MySQL_CONN():
        conn = MySQLdb.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='80233344',
            db='AgentPool',
        )
        return conn
