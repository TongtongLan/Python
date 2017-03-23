#!/usr/bin/python
# -*- coding: UTF-8 -*-

import schedule
import time
from datetime import datetime
import requests
from utils import MySQLexe
from utils import utils
import config
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import threading
from service import service_connect

REDIS_KEY_LAST_CHECK_IP_TIME = "last_check_ip_time"


class Proxy:

    def __init__(self, proxy_url):
        #代理IP的url
        self.proxy_url = proxy_url
        self.conn = service_connect.service_conn.MySQL_CONN()
        self.redis_client = config.redis_client


    def crawl_excuite(self):
        print ("exe......")
        content = self.HTTP_request(self.proxy_url).text
        soup = BeautifulSoup(content, "html.parser")

        ip = []
        for br in soup.find_all('br'):
            ip.append(br.next.strip())

        return ip
    def HTTP_request(self, proxy_url):
        session = requests.Session()
        session.mount('https://', HTTPAdapter(max_retries=5))
        session.mount('http://', HTTPAdapter(max_retries=5))
        response = session.get(proxy_url)
        return response


    def Crawl(self):
        proxy_list = self.crawl_excuite()

        if len(proxy_list) is 0:
            return

        #保存proxy_ip到MySQL中
        MySQLexe.MySQLexe().Insert_Proxy_List(self.conn, proxy_list)

    #获取IP代理池
    def GetIP(self):
        #如果当前IP池中的IP数量少于预设IP数,则开始爬取IP
        if MySQLexe.MySQLexe().Selete_Proxy_size(self.conn) < config.PROXY_SIZE:
            self.Crawl()

    #IP代理池自检
    def ChectIP(self):
        print ('调用一次checkIP')
        print (time.mktime(datetime.now().timetuple()))

        #从redis获取上次自检时间
        #如果小于预设自检间隔,退出自检
        last_check_time = self.redis_client.get(REDIS_KEY_LAST_CHECK_IP_TIME)
        current_time = time.mktime(datetime.now().timetuple())

        if last_check_time is not None and (current_time - float(last_check_time) < config.Check_Spacing_Time):
            return

        self.redis_client.set(REDIS_KEY_LAST_CHECK_IP_TIME, current_time)

        proxy_list = MySQLexe.MySQLexe().Selete_Proxy_List(self.conn)
        for ip in proxy_list:
            # 封装请求报头
            proxy = {'http': 'http://' + ip[0]}
            #print (config.check_IP_URL)

            try:
                # 发送请求获取返回码
                request = requests.get(config.check_IP_URL, proxies=proxy, timeout=1)
                if request.text is 'default':
                    print(ip)
            except Exception, e:
                # 删除数据表中一行
                #print ('error:', ip)

                MySQLexe.MySQLexe().delete_exe(self.conn, ip)

        print (time.mktime(datetime.now().timetuple()))





    #启动IP代理池获取
    def start(self):
        #获取代理池
        self.GetIP()
        def task():
            #IP自检
            self.ChectIP()
            #check ip every 60s
            schedule.every(60).seconds.do(self.ChectIP)
            while True:
                schedule.run_pending()
                time.sleep(1)

        thread = threading.Thread(target=task)
        thread.start()

proxy = Proxy("http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip")
proxy.start()