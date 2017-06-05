#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
from Utils import Utils, HTTPUtils, config, Encrypt


class Artists:
    def get_SongName(self, content):
        '''
        get songs name
        :param content:
        :return: song name
        '''
        return content.get_text()

    def parser_Html(self, content):
        '''
        解析 'http://music.163.com/artist?id=' 返回 HTML
        :param content: 网页 HTML 内容
        :return: 50首热门单曲 infolist
        '''
        infos_list = []
        for ul in HTTPUtils.HtmlParserUtils().get_TagList(content, 'ul', attrs={'class': 'f-hide'}):
            for li in HTTPUtils.HtmlParserUtils().get_TagList(ul, 'li'):
                # print get_SongName(li)
                for id in Utils.Utils().getStringByRe('[0-9]+', str(li.contents[0])):
                    # song_url = Get_Songs_RUrl.getSongUrl(id)
                    value = {}
                    value['song_name'] = self.get_SongName(li)
                    value['song_id'] = id
                    infos_list.append(value)
        return infos_list

    def get_ArtistHotList(self, id):
        '''
        通过ArtistId 获取 50首热门单曲
        :param id: ArtistId
        :return: 50首热门单曲 infolist
        '''
        url = config.ARTIST_URL + str(id)
        content = HTTPUtils.HtmlParserUtils().init_Html(HTTPUtils.HttpUtils().get_Request(url))
        hotList = self.parser_Html(content)
        return hotList

    def get_ArtistAlbumList(self, id):
        pass

    def get_ArtistMVList(self, id):
        pass

    def get_Artists(self, artistName):
        '''
        get Artists info By select artistName
        :param Artistname: name of Artist
        :return: Artists info (dict)
        '''
        data = HTTPUtils.HttpUtils().update_PostData(artistName, config.Artists_Type)
        response = HTTPUtils.HttpUtils().post_Request(config.SEARCH_URL, config.headers, data)
        # print json.dumps(response.json(), sort_keys=True, indent=4)
        code, result = HTTPUtils.JsonParserUtils().get_ResponseCodeAndResult(response)
        values = {}
        if code == 200:
            artist_Info_List = []
            values['artistCount'] = HTTPUtils.JsonParserUtils().get_JsonValue(result, 'artistCount')
            for artist in HTTPUtils.JsonParserUtils().get_JsonValue(result, 'artists'):
                value = HTTPUtils.JsonParserUtils().get_JsonValues(artist, 'artist', {},
                                       'id',
                                       'name',
                                       'mvSize',
                                       'albumSize')
                artist_Info_List.append(value)
            values['artistInfos'] = artist_Info_List
        return values


class Songs:
    DATA = config.data

    #SONGS_INFO = ['id', 'name', ['artists', ['id', 'name']], 'name', 'mvid']

    def get_SongsByName(self, songName):
        '''
        get songs info By select songName
        :param songName:
        :return: songs info (dict)
        '''
        data = HTTPUtils.HttpUtils().update_PostData(songName, config.Songs_Type)
        response = HTTPUtils.HttpUtils().post_Request(config.SEARCH_URL, config.headers, data)
        code, result = HTTPUtils.JsonParserUtils().get_ResponseCodeAndResult(response)
        values = {}
        values['songCount'] = HTTPUtils.JsonParserUtils().get_JsonValue(result, 'songCount')

        if code == 200:
            Songs_Info_List = []
            for song in HTTPUtils.JsonParserUtils().get_JsonValue(result, 'songs'):
                # print json.dumps(song, sort_keys=True, indent=4)
                Songs_Info = HTTPUtils.JsonParserUtils().get_JsonValues(song, 'song', {},
                                            'id',
                                            'name',
                                            ['album', ['id', 'name']],
                                            ['artists', ['id', 'name']],
                                            'mvid')
                Songs_Info_List.append(Songs_Info)
            values['songs'] = Songs_Info_List
        return values

    def get_SongBySongID(self, songId):
        '''
        get song info By select songId
        :param songId:
        :return: song info (dict)
        '''
        pass

    def getCsrf_token(self, songId):
        '''
        获取加密后的post请求参数
        :param songId:
        :return: post 参数
        '''
        secKey = Encrypt.Encrypt().createSecretKey(config.Encrypt_BS)

        first_param = "{\"ids\":\"[" + str(songId) + "]\",\"br\":128000,\"csrf_token\":\"\"}"
        # 通过AES加密
        encText = Encrypt.Encrypt().aesEncrypt(Encrypt.Encrypt().aesEncrypt(first_param, config.Encrypt_nonce), secKey)
        encSecKey = Encrypt.Encrypt().rsaEncrypt(secKey, config.Encrypt_pubKey, config.Encrypt_modulus)

        data = {
            'params': encText,
            'encSecKey': encSecKey
        }

        return data

    def getSongUrl(self, songId):
        '''
        获取当前 songId 对应歌曲url
        :param songId:
        :return: 歌曲url
        '''
        # get csrf_token
        data = self.getCsrf_token(songId)
        # post request
        response = HTTPUtils.HttpUtils().post_Request(config.GET_SONGURL_url, config.headers, data)

        return response.json()['data'][0]['url']


class Albums:

    def get_Albums(self, albumName):
        '''
        get songs info By select albumName
        :param albumName:
        :return: songs info
        '''

        data = HTTPUtils.HttpUtils().update_PostData(albumName, config.Albums_Type)
        response = HTTPUtils.HttpUtils().post_Request(config.SEARCH_URL,
                                                      config.headers,
                                                      data)
        for album in response.json()['result']['albums']:
            print album
            d1 = json.dumps(album, sort_keys=True, indent=4)
            print d1

class Lyrics:
    def get_LyricsToSongs(self, lyrics):
        '''
        get songs info By select lyrics
        :param lyrics:
        :return: songs info
        '''
        response = HTTPUtils.HttpUtils().post_Request(HTTPUtils.HttpUtils().update_PostData(lyrics, config.Lyrics_Type))
        result = response.json()['result']
        if result['songCount'] != 0:
            for lyricsToSong in result['songs']:
                # print lyricsToSong
                d1 = json.dumps(lyricsToSong, sort_keys=True, indent=4)
                print d1
                return d1
        else:
            print 'No songs!'


def test_get_songs(songname):
    for key, value in Songs().get_SongsByName(songname).items():
        print key
        if isinstance(value, list):
            for v in value:
                print v
        else:
            print value

def test_get_artists(artistname):
    for key, value in Artists().get_Artists(artistname).items():
        print key
        if isinstance(value, list):
            for v in value:
                print v
        else:
            print value

def test_get_Albums(alumbName):
    result = Albums().get_Albums(alumbName)
    print type(result)
    if isinstance(result, dict):
        for key, value in result:

            print key
            print value
    else:
        print result


test_get_songs('gulou')
test_get_artists('张伟')
test_get_Albums('吉姆餐厅')




