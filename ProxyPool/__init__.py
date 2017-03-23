#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
爬取 IP 代理并保存在 MySQL
'''
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import MySQLdb
import ChectIpProxy


class Proxy:

    def __init__(self, proxy_url, conn):
        self.proxy_url = proxy_url
        self.conn = conn



    def HTTP_request(self, proxy_url):
        session = requests.Session()
        session.mount('https://', HTTPAdapter(max_retries=5))
        session.mount('http://', HTTPAdapter(max_retries=5))
        response = session.get(proxy_url)
        return response


    def excuite(self):
        print ("exe......")
        content = self.HTTP_request(self.proxy_url).text
        soup = BeautifulSoup(content, "html.parser")

        ip = []
        for br in soup.find_all('br'):
            ip.append(br.next.strip())

        return ip

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

    # DB操作方法
    def MySQL_exe(self, proxy_ip_list):

        conn = self.conn

        # 选择数据库
        conn.select_db('AgentPool');

        # 获取操作游标
        cursor = conn.cursor()

        # 插入记录
        cursor.execute("SELECT * from ProxyPool_info1")
        for ip in proxy_ip_list:
            cursor.execute("insert into ProxyPool_info1 values ('"+ip+"')");

        # 提交到数据库执行
        conn.commit()


print('123')
conn = Proxy.MySQL_CONN()
test = Proxy('http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip' ,conn)
test.MySQL_exe (test.excuite())

print (ChectIpProxy.ChectIpProxy().GetIpCollection(conn))
ChectIpProxy.ChectIpProxy().get_valid_proxies(ChectIpProxy.ChectIpProxy().GetIpCollection(conn), conn)