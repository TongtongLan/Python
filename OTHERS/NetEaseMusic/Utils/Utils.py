#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
class Utils:

    def get_CommandLineInput(self, hint):
        commandLineInput = raw_input(hint)
        return commandLineInput

    def output_Info(self, infos):
        if isinstance(infos, list):
            for info in infos:
                print info
        else:
            print infos

    def getStringByRe(self, pattern, string):
        return re.findall(pattern, string)

    def initialize_MainInterface(self):
        print '-' * 100
        print '0——回退'
        print '1——查询歌曲'
        print '2——查询歌手'
        print '3——查询专辑'

    def initialize_SecondInterface(self, case):
        if case == 'song':
            print '-' * 100
            print '0——回退'
            print '1——重查'
            print '2——选择歌曲编号'
        else:
            pass

    def initialize_ThirdInterface(self, case):
        if case == 'song':
            print '-' * 100
            print '0——回退'
            print '1——播放'
            print '2——查看歌手, 通过歌手id获取歌手信息'
            print '3——查看专辑, 通过专辑ID获取专辑信息'
        else:
            pass