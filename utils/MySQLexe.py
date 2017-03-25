#!/usr/bin/python
# -*- coding: UTF-8 -*-

from service import config
import _mysql_exceptions
class MySQLexe:

    @staticmethod
    def Get_update_time():

        return

    def Get_create_time(self):

        pass

    def Get_Ip(self):

        pass


    @staticmethod
    def delete_exe(conn, ip):
        # 删除数据表中一行
        conn.cursor().execute("delete from " + config.PROXYPOOL_TABLENAME + " where ip = '" + ip[0] + "'")
        conn.commit()

    def Selete_Proxy_List(self, conn):
        cursor = conn.cursor()
        collection = cursor.execute("select ip from " + config.PROXYPOOL_TABLENAME)

        content = []
        for row in cursor.fetchall():
            "返回整行数据tuple类型"
            content.append(row)

        return content




    def Selete_Proxy_size(self, conn):
        collection = conn.cursor().execute("select * from ProxyPool_info1")
        return collection

    def Insert_Proxy_List(self, conn, proxy_list):
        for proxy_info in proxy_list:
            print proxy_info
            try:
                conn.cursor().execute(
                    "INSERT INTO " + config.PROXYPOOL_TABLENAME + " VALUES ('" + proxy_info['ip'] + "', '" + str(
                        proxy_info['ip_create_time']) + "', '" + proxy_info['is_high_quality'] + "')")
            except _mysql_exceptions.IntegrityError, e:
                print e
        # 提交到数据库执行
        conn.commit()
