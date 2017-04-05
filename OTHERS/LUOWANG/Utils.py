#!/usr/bin/python
# -*- coding: UTF-8 -*-

import config
import tkFileDialog
from bs4 import BeautifulSoup
import requests

def getSongIssueNumber():
    songIssueNumber = ''
    try:
        songIssueNumber = int(getTerminalInputInfo())
    except:
        print u"值有误,请输入大于零的音乐期刊号:\n>"
        getSongIssueNumber()

    return songIssueNumber

def getSongsSaveDirectory():
    songsSaveDirectory = tkFileDialog.askdirectory()
    return songsSaveDirectory


def getTerminalInputInfo():
    TerminalInputInfo = raw_input()
    return TerminalInputInfo

def isIssueNumGreaterThanMax(songIssueNumber):
    if songIssueNumber > config.SONG_ISSUE_MAX:
        return True
    return False

def isIssueNumLessThanMin(songIssueNumber):
    if songIssueNumber <= config.SONG_ISSUE_MIN:
        return True
    return False

def isSongsSaveDirectoryNull(songsSaveDirectory):
    if songsSaveDirectory is '':
        return True
    return False

def getContentByHtml5lib(responseContent):
    responseContent = BeautifulSoup(responseContent, 'html5lib')
    return responseContent

def getResponseContent(issueUrl):
    # get html
    response = requests.get(issueUrl)
    # 设置requests编码
    response.encoding = 'utf-8'
    responseContent = response.text
    return responseContent

def getIssueUrl(songIssueNumber):
    issueUrl = config.BASE_URL + str(songIssueNumber)
    return issueUrl