#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
check ProxyPool 中的IP
'''

import  requests

class ChectIpProxy:


    @staticmethod
    # 获取数据库中的代理IP
    def GetIpCollection(conn):

        cursor = conn.cursor()

        collection = cursor.execute("select * from ProxyPool_info1")

        content = []
        for row in cursor.fetchall():
            "返回整行数据tuple类型"
            content.append(row)

        return content

    def get_valid_proxies(self, Proxy_list, conn):

        url = "http://lwons.com/wx"
        print (Proxy_list)

        for ip in Proxy_list:
            print (ip)
            print (type(ip))

            proxy = {'http':'http://' + ip[0]}

            succeed = False

            try:
                request = requests.get(url, proxies = proxy, timeout=1)
                if request.text is 'default':
                    succeed = True

            except Exception, e:
                print ('error:',ip)
                cursor = conn.cursor()
                # 删除数据表中一行
                cursor.execute("delete from ProxyPool_info1 where ip = '" + ip[0] +"'")
                conn.commit()
                succeed = False

            if succeed:
                print ('succeed:',ip)










