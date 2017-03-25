#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
创建数据表
'''
import service_connect

def ProxyPool_Table(conn):

    sql = 'create table ProxyPool_info (ip varchar(20) PRIMARY KEY, ip_create_time varchar(20), is_high_quality varchar(20));'
    conn.cursor().execute(sql)

ProxyPool_Table(service_connect.service_conn.MySQL_CONN())