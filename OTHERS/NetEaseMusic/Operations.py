#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Utils import Utils
class selectOperations:

    HINT_SONG_NUM = 'Please enter the song number :'

    def __init__(self):
        pass

    def print_Results(self, results):
        pass

    def print_songs(self, results):
        for key, value in results.items():
            print key
            if isinstance(value, list):
                for v in value:
                    print v
            else:
                print value

    def print_number(self, results, number):
        '''
        print 第 number 个数据
        :param results:
        :param number:
        :return:
        '''
        if not isinstance(number, int):
            number = int(number)
        if isinstance(results, list):
            try:
                #print results[number]
                for k, v in results[number].items():
                    print k, v
            except:
                print 'index out!'
        elif isinstance(results, dict):
            for key, value in results.items():
                if isinstance(value, list):
                    try:
                        #print value[number]
                        for k, v in value[number].items():
                            print k, v
                    except:
                        print 'index out!'

    def select_Songs(self, songname):
        # select songname
        result = Get_Artist_Id.get_Songs(songname)
        # output results
        self.print_songs(result)
        while 1:
            # diaoyong xuanze jiemian
            Utils.Utils().initialize_SecondInterface('song')
            number = Utils.Utils().get_CommandLineInput(self.HINT_SONG_NUM)
            if number == '0':
                return
            elif number == '1':
                self.select_Songs(songname)
            elif number == '2':
                song_num = Utils.Utils().get_CommandLineInput(self.HINT_SONG_NUM)
                self.print_number(result, song_num)
                while 1:
                    Utils.Utils().initialize_ThirdInterface('song')
                    thirdNumber = Utils.Utils().get_CommandLineInput(self.HINT_SONG_NUM)
                    if thirdNumber == '0':
                        # 回退
                        break
                    elif thirdNumber == '1':
                        # 播放
                        pass
                    elif thirdNumber == '2':
                        # 查看歌手, 通过歌手id获取歌手信息
                        pass
                    elif thirdNumber == '3':
                        # 查看专辑, 通过专辑ID获取专辑信息
                        pass
                    else:
                        continue
            else:
                print 'error!'

    def select_Artlist(self, artistname):
        pass

    def select_zhuanji(self, name):
        pass