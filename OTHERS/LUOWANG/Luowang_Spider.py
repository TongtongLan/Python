#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
download the musics from LUOWANG
'''
import requests
from bs4 import BeautifulSoup
from DownLoad_mp3 import Download_Mp3
import sys
import threading
import time
import Utils
class luowang_spider():

    BASE_URL = 'http://www.luoo.net/music/'
    BASE_SONG_DOWNLOAD_URL = "http://mp3-cdn.luoo.net/low/luoo/"
    SONG_ISSUE_MAX = 904
    NULL = ''
    HTML_LABEL_LI = 'li'
    HTML_LABEL_A = 'a'
    HTML_LABEL_SPAN = 'span'

    def init(self):
        print u"请输入音乐期刊号:\n>"
        songIssueNumber = self.NULL
        while(True):
            songIssueNumber = Utils.getSongIssueNumber()
            if Utils.isIssueNumGreaterThanMax(songIssueNumber):
                print u"输入的数字大于最大的期刊号，请重新输入：\n"
                continue
            elif Utils.isIssueNumLessThanMin(songIssueNumber):
                print u"输入的数字必须大于0，请重新输入：\n"
            else:
                break
        print u"请选择保存路径:\n>"
        time.sleep(1)
        songsSaveDirectory = self.NULL
        cancelSaveFlag = 0
        while Utils.isSongsSaveDirectoryNull(songsSaveDirectory) and cancelSaveFlag < 1:
            cancelSaveFlag += 1
            songsSaveDirectory = Utils.getSongsSaveDirectory()

        return songIssueNumber, songsSaveDirectory

    def parseIssuePage(self, responseContent):
        # 用html5lib解析网页
        responseContent = Utils.getContentByHtml5lib(responseContent)

        includeLiLabelList = responseContent.findAll(self.HTML_LABEL_LI, {"class": "track-item rounded"})

        songsInfoList = []

        for li in includeLiLabelList:
            songName = li.find(self.HTML_LABEL_A, {"class": 'trackname btn-play'}).text
            singer = li.find(self.HTML_LABEL_SPAN, {"class": 'artist btn-play'}).text
            songInfo = {
                "songName": songName,
                "singer": singer
            }

            songsInfoList.append(songInfo)

        return songsInfoList

    def crawlExecute(self, songIssueNumber):

        # set url
        issueUrl = self.BASE_URL + str(songIssueNumber)

        responseContent = Utils.getResponseContent(issueUrl)

        songsInfoList = self.parseIssuePage(responseContent)

        return songsInfoList

    def Crawl(self):
        songIssueNumber, songsSaveDirectory = self.init()
        if songsSaveDirectory is self.NULL:
            print u"取消下载"
            return
        songsInfoList = self.crawlExecute(songIssueNumber)
        thread = []
        SongDownloadUrl = self.NULL

        print len(songsInfoList)

        for songInfo in songsInfoList:
            songNumber = songsInfoList.index(songInfo)+1
            if songNumber < 10:
                SongDownloadUrl = self.BASE_SONG_DOWNLOAD_URL + "radio" + str(songIssueNumber) + "/0" + str(
                    songNumber) + ".mp3"
            elif songNumber >= 10:
                SongDownloadUrl = self.BASE_SONG_DOWNLOAD_URL + "radio" + str(songIssueNumber) + "/" + str(
                    songNumber) + ".mp3"

            SaveSongFileRout = songsSaveDirectory + "/" + songInfo.get("songName").replace("/", "\\").decode('utf-8') + ".mp3"
            if len(thread) < 15:
                t = threading.Thread(target=Download_Mp3().download_Mp3(SongDownloadUrl, SaveSongFileRout))
                thread.append(t)
                t.setDaemon(True)
                print("start one thread")
                t.start()

reload(sys)
sys.setdefaultencoding('utf-8')
luowang_spider().Crawl()
