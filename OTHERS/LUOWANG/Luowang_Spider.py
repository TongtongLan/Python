#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
download the musics from LUOWANG
'''
import requests
from bs4 import BeautifulSoup
from DownLoad_mp3 import download_mp3
import os
import sys
import threading
import time
import tkFileDialog
basePath = os.path.join(os.getcwd(), r'luowang')
class luowang_spider():

    BASE_URL = 'http://www.luoo.net/music/'
    BASE_DOWNLOAD_URL = "http://mp3-cdn.luoo.net/low/luoo/"
    PAGE_MAX = 904

    def init(self):
        print u"请输入音乐期刊号:\n>"
        vol=""
        while(True):
            vol = raw_input()
            try:
                page_from = int(vol)
            except:
                print u"值有误,请输入大于零的音乐期刊号:\n>"
                continue
            if page_from > self.PAGE_MAX:
                print u"输入的数字大于最大的期刊号，请重新输入：\n"
                continue
            elif page_from <=0:
                print u"输入的数字必须大于0，请重新输入：\n"
            else:
                break
        print u"请选择保存路径:\n>"
        time.sleep(1)
        directory = tkFileDialog.askdirectory()
        i = 0
        while directory is "" and i < 1:
            i+=1
            directory = tkFileDialog.askdirectory()

        return vol,directory

    def crawl_execute(self, issue):

        # set url
        URL = self.BASE_URL+str(issue)
        # get html
        response = requests.get(URL)
        # 设置requests编码
        response.encoding = 'utf-8'
        content = response.text
        # 用html5lib解析网页
        html = BeautifulSoup(content, 'html5lib')
        li_list = html.findAll('li', {"class": "track-item rounded"})

        issue_list =  []

        for li in li_list:

            song_name = li.find('a',{"class":"trackname btn-play"}).text
            song_songer = li.find('span',{"class":'artist btn-play'}).text
            song_list = {
                "song_name" : song_name,
                "song_songer" : song_songer
            }

            issue_list.append(song_list)

        return issue_list

    def Crawl(self):
        issue, directory = self.init()
        if directory is "":
            print u"取消下载"
            return
        issue_list = self.crawl_execute(issue)
        thread =[]

        for song in issue_list:
            index = issue_list.index(song)+1
            if index<10:
                download_url = self.BASE_DOWNLOAD_URL + "radio" + str(issue) + "/0" + str(
                    index) + ".mp3"
            elif index>= 10:
                download_url = self.BASE_DOWNLOAD_URL + "radio" + str(issue) + "/" + str(
                    index) + ".mp3"
            print download_url
            print (song.get("song_name"))

            filename = directory + "/"+song.get("song_name").replace ("/","\\").decode('utf-8') + ".mp3"
            print filename
            #download_mp3().download(download_url, filename)
            if len(thread)<10:
                t = threading.Thread(target=download_mp3().download(download_url, filename))
                thread.append(t)
                t.setDaemon(True)
                print("start one thread")
                t.start()

reload(sys)
sys.setdefaultencoding('utf-8')
luowang_spider().Crawl()
