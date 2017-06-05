#!/usr/bin/env python
# -*- coding: utf-8 -*-
ARTIST_URL = 'http://music.163.com/artist?id='
SEARCH_URL = 'http://music.163.com/api/search/get'
GET_SONGURL_url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='

headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/'
}


Albums_Type = 10
Songs_Type = 1
Artists_Type = 100
Lyrics_Type = 1006

# 修改type值可以改变查询方式
data = {
    's': '我今生何求为你',
    'type': 1009,
    'offset': 0,
    'total': True,
    'limit': 60}

Encrypt_modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
Encrypt_nonce = '0CoJUm6Qyw8W8jud'
Encrypt_pubKey = '010001'
Encrypt_BS = 16
