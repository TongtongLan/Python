#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import MySQLdb


class Proxy:

    def __init__(self, proxy_url):
        self.proxy_url = proxy_url
        self.conn = None


    def HTTP_request(self, proxy_url):
        session = requests.Session()
        session.mount('https://', HTTPAdapter(max_retries=5))
        session.mount('http://', HTTPAdapter(max_retries=5))
        response = session.get(proxy_url)
        return response


    def excuite(self):

        content = self.HTTP_request(self.proxy_url).text
        soup = BeautifulSoup(content, "html.parser")

        ip = []
        for br in soup.find_all('br'):
            ip.append(br.next.strip())

        return ip

    def MySQL_CONN(self):
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

        conn = self.MySQL_CONN()

        # 选择数据库
        conn.select_db('AgentPool');

        # 获取操作游标
        cursor = conn.cursor()

        # 执行SQL,创建一个数据表.
        #cursor.execute("""create table ProxyPool_info1(ip varchar(100)) """)
        # 插入记录
        cursor.execute("SELECT * from ProxyPool_info1")
        for ip in proxy_ip_list:
            cursor.execute("insert into ProxyPool_info1 values ('"+ip+"')");

        # 提交到数据库执行
        conn.commit()





test = Proxy('http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip')
test.MySQL_exe (test.excuite())