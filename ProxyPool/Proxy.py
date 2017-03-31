#!/usr/bin/python
# -*- coding: UTF-8 -*-

import schedule
import time
from datetime import datetime
import requests
from utils import MySQLexe
import config
import threading
from service import service_connect
import ProxyStrategy


REDIS_KEY_LAST_CHECK_IP_TIME = "last_check_ip_time"


class Proxy:

    def __init__(self):
        #代理IP的url
        self.conn = service_connect.service_conn.MySQL_CONN()
        self.redis_client = config.redis_client


    def random_choice_proxy(self):
        pass

    #开启爬取指令
    def Crawl(self):
        print('crawl()......')
        proxy_list = ProxyStrategy.Get66ipProxyStrategy().crawl_execute()
        proxy_list = proxy_list + ProxyStrategy.GetNNProxyStrategy().crawl_execute()
        proxy_list = proxy_list + ProxyStrategy.GetWNProxyStrategy().crawl_execute()
        proxy_list = proxy_list + ProxyStrategy.GetWTProxyStrategy().crawl_execute()

        if len(proxy_list) is 0:
            return
        print ('save   mysql.....')

        #保存proxy_ip到MySQL中
        MySQLexe.MySQLexe().Insert_Proxy_List(self.conn, proxy_list)

    #获取IP代理池
    def GetIP(self):
        #如果当前IP池中的IP数量少于预设IP数,则开始爬取IP
        print('getip()......')
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

        #if last_check_time is not None and (current_time - float(last_check_time) < config.Check_Spacing_Time):
            #return

        self.redis_client.set(REDIS_KEY_LAST_CHECK_IP_TIME, current_time)

        proxy_list = MySQLexe.MySQLexe().Selete_Proxy_List(self.conn)
        for ip in proxy_list:
            # 封装请求报头
            proxy = {'http': 'http://' + ip[0]}

            try:
                requests.get(config.check_IP_URL, proxies=proxy, timeout=5)
            except:
                print ('error:', ip)
                MySQLexe.MySQLexe().delete_exe(self.conn, ip)
            else:
                print ('success:', ip)

        print (time.mktime(datetime.now().timetuple()))


    #启动IP代理池获取
    def start(self):
        #获取代理池
        self.GetIP()
        def task():
            #IP自检
            self.ChectIP()
            #check ip every 60m
            schedule.every(60).minutes.do(self.ChectIP)
            while True:
                schedule.run_pending()
                time.sleep(1)

        thread = threading.Thread(target=task)
        thread.start()

proxy = Proxy()
proxy.start()