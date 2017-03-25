#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
IP代理爬取机制
'''

from requests.adapters import HTTPAdapter
import requests
from bs4 import BeautifulSoup
from utils import HTTPHeaders
from utils import config
import time
from datetime import datetime

class GetProxyStrategy(object):

    URL = ''

    def __init__(self):
        self.content = ''
        self.proxy_list = []


    def HTTP_request(self, proxy_url):
        session = requests.Session()
        session.mount('https://', HTTPAdapter(max_retries=5))
        session.mount('http://', HTTPAdapter(max_retries=5))
        response = session.get(proxy_url, headers=HTTPHeaders.HTTPHeader().GetHttpHeader(), timeout=config.TIMEOUT)

        return response

    def crawl_execute(self):
        print ("exe......")
        self.content = self.HTTP_request(self.URL).text



class Get66ipProxyStrategy(GetProxyStrategy):

    URL = 'http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip'

    def HTTP_request(self, proxy_url):
        session = requests.Session()
        session.mount('https://', HTTPAdapter(max_retries=5))
        session.mount('http://', HTTPAdapter(max_retries=5))
        response = session.get(proxy_url, timeout=config.TIMEOUT)

        return response
    def crawl_execute(self):
        self.content = self.HTTP_request(self.URL).text
        self.proxy_list = self.parse(self.content)
        print self.proxy_list
        return self.proxy_list

    def parse(self, content):
        soup = BeautifulSoup(content, "html.parser")
        proxy_info = {}

        proxy_list = []
        for br in soup.find_all('br'):
            current_time = time.mktime(datetime.now().timetuple())
            proxy_info = {'ip': br.next.strip(),
                          'ip_create_time': current_time,
                          'is_high_quality': 'False'
                          }
            proxy_list.append(proxy_info)

        return proxy_list


class GetxicidailiProxyStrategy(GetProxyStrategy):
    SPEED = 5

    def crawl_execute(self):
        #print ('GetxicidailiProxyStrategy.crawl_execute().....')
        super(GetxicidailiProxyStrategy, self).crawl_execute()
        self.proxy_list = self.parse(self.content)
        #print ('GetxicidailiProxyStrategy....')
        #print (self.proxy_list)
        return self.proxy_list

    def parse(self, content):
        s='高匿'
        proxy_info_list = []
        soup = BeautifulSoup(content, "html5lib")
        tbody = soup.findAll('tbody')
        for tb in tbody:
            tr_list = tb.findAll('tr')
            for tr in tr_list:
                td_list = tr.findAll('td')
                if td_list == []:
                    continue
                address = ''
                port = ''
                is_high_quality = True
                proxy_info = {}
                for num, data in enumerate(td_list):
                    if num == 1:
                        address = data.getText()
                        #print (num, data.getText())
                    if num == 2:
                        port = data.getText()
                    if num == 4:
                        #print (num, data.getText())
                        is_high_quality = data.getText().encode('utf-8') == s
                        if not is_high_quality:
                            continue
                        current_time = time.mktime(datetime.now().timetuple())
                        proxy_info = {'ip': address + ':' + port,
                              'ip_create_time': current_time,
                              'is_high_quality': str(is_high_quality)
                              }
                        #print proxy_info
                if is_high_quality:
                    proxy_info_list.append(proxy_info)

                    #print (num, data.getText())
                    #print (address, port)
                    #print (ip)
        #print ('parse........')
        #print (proxy_info_list)




        return proxy_info_list



class GetWNProxyStrategy(GetxicidailiProxyStrategy):
    SPEED = 80
    URL = 'http://www.xicidaili.com/wn/'

    def crawl_execute(self):
        super(GetWNProxyStrategy, self).crawl_execute()
        return self.proxy_list


class GetNNProxyStrategy(GetxicidailiProxyStrategy):
    SPEED = 85

    URL = 'http://www.xicidaili.com/nn/'

    def crawl_execute(self):
        #print ('GetNNProxyStrategy.crawl_execute()......')
        super(GetNNProxyStrategy, self).crawl_execute()
        return self.proxy_list

class GetWTProxyStrategy(GetxicidailiProxyStrategy):
    SPEED = 88
    URL = 'http://www.xicidaili.com/wt/'
    def crawl_execute(self):
        super(GetWTProxyStrategy, self).crawl_execute()

        return self.proxy_list



