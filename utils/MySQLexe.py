#!/usr/bin/python
# -*- coding: UTF-8 -*-

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
        conn.cursor().execute("delete from ProxyPool_info1 where ip = '" + ip[0] + "'")
        conn.commit()

    def Selete_Proxy_List(self, conn):
        cursor = conn.cursor()
        collection = cursor.execute("select * from ProxyPool_info1")

        content = []
        for row in cursor.fetchall():
            "返回整行数据tuple类型"
            content.append(row)

        return content




    def Selete_Proxy_size(self, conn):
        collection = conn.cursor().execute("select * from ProxyPool_info1")
        return collection

    def Insert_Proxy_List(self, conn, proxy_list):
        for ip in proxy_list:
            conn.cursor().execute("insert into ProxyPool_info1 values ('"+ip+"')");

        # 提交到数据库执行
        conn.commit()
