#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageFilter, ImageEnhance
import os
os.chdir('/home/tongtong/文档/libsvm-3.22')
from svmutil import *

class TrainSet:
    # ---------------------------------------------------------------------------------------------
    # 图片预处理
    def blockToWrite(self, img):
        '''
        将图片中黑白像素点互相转化, 黑底白字 -> 白底黑字
        :param img:
        :return:
        '''
        img_array = img.load()
        for i in xrange(img.size[0]):
            for j in xrange(img.size[1]):
                try:
                    rgb_value = img_array[i, j]
                    r, g, b = rgb_value[0], rgb_value[1], rgb_value[2]
                    if r == 0 and g == 0 and b == 0:
                        img_array[i, j] = (255, 255, 255, 255)
                    elif r == 255 and g == 255 and b == 255:
                        img_array[i, j] = (0, 0, 0, 255)
                    print img.getpixel((i, j))
                except:
                    print 'out'
        return img

    def blockToWrite2(self, img):
        '''
        将图片中黑白像素点互相转化, 白色之外的像素点都转化为黑色像素点（可以试试黑色之外像素点转化为白素像素会不会提高识别率
        :param img:
        :return:
        '''
        img_array = img.load()
        for i in xrange(img.size[0]):
            for j in xrange(img.size[1]):
                try:
                    rgb_value = img_array[i, j]
                    r, g, b = rgb_value[0], rgb_value[1], rgb_value[2]
                    if r == 255 and g == 255 and b == 255:
                        img_array[i, j] = (255, 255, 255, 255)
                    else:
                        img_array[i, j] = (0, 0, 0, 255)
                        # print img.getpixel((i, j))
                except:
                    print 'out'
        return img

    def Caculate_X(self, im):
        '''
        依据图片像素颜色计算X轴投影
        :param im:
        :return:
        '''
        Image_Value = []
        for i in range(im.size[0]):
            Y_pixel = 0
            for j in range(im.size[1]):
                rgb_value = im.getpixel((i, j))
                r, g, b = rgb_value[0], rgb_value[1], rgb_value[2]
                if r == 0 and g == 0 and b == 0:
                    # print '1'
                    temp_value = 1
                else:
                    # print '0'
                    temp_value = 0
                Y_pixel = Y_pixel + temp_value
            Image_Value.append(Y_pixel)
        return Image_Value

    def Caculate_Y(self, im):
        '''
        依据图片像素颜色计算Y轴投影
        :param im:
        :return:
        '''
        Image_Value = []
        for i in range(im.size[1]):
            Y_pixel = 0
            for j in range(im.size[0]):
                try:
                    rgb_value = im.getpixel((j, i))
                    # rgb_value = im.getpixel((i, j))
                    r, g, b = rgb_value[0], rgb_value[1], rgb_value[2]
                    if r == 0 and g == 0 and b == 0:
                        # print '1'
                        temp_value = 1
                    else:
                        # print '0'
                        temp_value = 0
                    Y_pixel = Y_pixel + temp_value
                except:
                    print 'out'

            Image_Value.append(Y_pixel)
        return Image_Value

    def Cut_Y(self, im):
        '''
        横向切割，依据Y轴的投影，去除上下非字符部分，并返回切割点的坐标
        :param im:
        :return:
        '''
        Image_Value = self.Caculate_Y(im)
        print Image_Value
        Y_value = []
        List0 = []
        List1 = []
        ListRow0 = []
        ListRow1 = []
        for i in range(len(Image_Value)):
            if Image_Value[i] == 0 and len(ListRow1) == 0:  # 数字左侧的空白列
                ListRow0.append(i)
            elif Image_Value[i] == 0 and len(ListRow1) > 0:  # 数字右侧的空白列
                List1.append(ListRow1)
                ListRow1 = []
                ListRow0.append(i)
            elif Image_Value[i] > 0 and len(ListRow0) > 0:  # 数字列
                List0.append(ListRow0)
                ListRow0 = []
                ListRow1.append(i)
            elif Image_Value[i] > 0 and len(ListRow0) == 0:  # 数字列
                ListRow1.append(i)

        if len(List1) == 1:  # 如果只有1个数字右侧的空白列
            Y_value.append(List1[0][0])
            Y_value.append(List1[0][(len(List1[0]) - 1)])
        else:
            Y_value.append(List1[0][0])
            Y_value.append(List1[len(List1) - 1][(len(List1[0]) - 1)])
        return Y_value

    def Cut_X(self, im):
        '''
        纵向切割，依据X轴的投影，将图片切割为4张图片，并返回切割点的坐标
        :param im:
        :return:
        '''
        Image_Value = self.Caculate_X(im)
        print Image_Value
        X_value = []
        List0 = []
        List1 = []
        ListRow0 = []
        ListRow1 = []
        for i in range(len(Image_Value)):
            if Image_Value[i] == 0 and len(ListRow1) == 0:  # 数字左侧的空白列
                ListRow0.append(i)
            elif Image_Value[i] == 0 and len(ListRow1) > 0:  # 数字右侧的空白列
                List1.append(ListRow1)
                ListRow1 = []
                ListRow0.append(i)
            elif Image_Value[i] > 0 and len(ListRow0) > 0:  # 数字列
                List0.append(ListRow0)
                ListRow0 = []
                ListRow1.append(i)
            elif Image_Value[i] > 0 and len(ListRow0) == 0:  # 数字列
                ListRow1.append(i)

        if len(List1) == 1:  # 如果只有1个数字右侧的空白列，放弃切割
            for i in range(4):
                X_value.append(1 + 12 * i)  #
                X_value.append(12 * i + 12)
        elif len(List1) == 2:  # 如果只有2个数字右侧的空白列，放弃切割
            for i in range(4):
                X_value.append(12 * i)  #
                X_value.append(12 * i)
        elif len(List1) == 3:  # 如果有3个数字右侧的空白列，将数字列中最长的那段值进行拆分，拆分点在X轴投影的大于第五位后的第一个最低点。

            Max_index = self.Max_Index(List1)
            for i in range(len(List1)):
                if i == Max_index:
                    #
                    index = self.Cut_Two(List1[i], Image_Value)
                    X_value.append(List1[i][0])
                    X_value.append(List1[i][index])
                    X_value.append(List1[i][(index + 1)])
                    X_value.append(List1[i][(len(List1[i]) - 1)])
                else:
                    X_value.append(List1[i][0])
                    X_value.append(List1[i][(len(List1[i]) - 1)])
        elif len(List1) == 4:  # 4个空白列
            for i in range(len(List1)):
                X_value.append(List1[i][0])
                X_value.append(List1[i][(len(List1[i]) - 1)])
        elif len(List1) == 5:  # 如果有5个数字右侧的空白列，取长度最长的4段。

            Min_index = self.Min_Index(List1)
            for i in range(len(List1)):
                if i <> Min_index:
                    X_value.append(List1[i][0])
                    X_value.append(List1[i][(len(List1[i]) - 1)])
        elif len(List1) > 5:  # 大于5个直接放弃切割
            for i in range(4):
                X_value.append(1 + 12 * i)  #############
                X_value.append(12 * i + 12)
        return X_value

    def Cut_Two(self, ListRow, Image_Value):
        '''
        分割两个紧挨的数字
        :param ListRow:
        :param Image_Value:
        :return:
        '''
        index = 0
        start = 0
        if len(ListRow) >= 15:
            start = 3
        for i in range((start), (len(ListRow) - 1)):
            if Image_Value[ListRow[i]] <= Image_Value[ListRow[(i - 1)]] and Image_Value[ListRow[i]] <= 2:  #
                index = i
                break

        return index

    def Max_Index(self, List1):
        '''
        返回矩阵各行最大值位置的函数，以便找到有颜色的列中X轴投影最大的地方
        :param List1:
        :return:
        '''
        Max = 0
        Max_index = 0
        for i in range(len(List1)):
            if len(List1[i]) > Max:
                Max = len(List1[i])
                Max_index = i
        return Max_index

    def Min_Index(self, List1):
        '''
        返回矩阵各行最小值位置的函数，以便找到有颜色的列中X轴投影最小的地方
        :param List1:
        :return:
        '''
        Min = 50
        Min_index = 0
        for i in range(len(List1)):
            if len(List1[i]) < Min:
                Min = len(List1[i])
                Min_index = i

        return Min_index


    def binary(self, dir_pic, save_dir):
        '''
        图片二值化
        :param dir_pic:
        :return:
        '''
        i = 0
        for f in os.listdir(dir_pic):
            if f.endswith('.png'):
                img = Image.open(dir_pic + f)
                img = img.convert("RGBA")
                img = self.blockToWrite2(img)
                pixdata = img.load()
                for y in xrange(img.size[1]):
                    for x in xrange(img.size[0]):
                        if pixdata[x, y][0] < 90:
                            pixdata[x, y] = (0, 0, 0, 255)
                for y in xrange(img.size[1]):
                    for x in xrange(img.size[0]):
                        if pixdata[x, y][1] < 136:
                            pixdata[x, y] = (0, 0, 0, 255)
                for y in xrange(img.size[1]):
                    for x in xrange(img.size[0]):
                        if pixdata[x, y][2] > 0:
                            pixdata[x, y] = (255, 255, 255, 255)
                img = self.blockToWrite(img)
                img.save(save_dir + f)
                x_value = self.Cut_X(img)
                y_value = self.Cut_Y(img)
                self.get_matrix(x_value, y_value, img, i)
                i += 1

    def get_matrix(self, X_value, Y_value, img, img_len):
        '''
        根据二值化的验证码创建字模,存储num目录中
        :param X_value:
        :param Y_value:
        :param img:
        :param img_len:
        :return:
        '''
        for i in range(0, len(X_value), 2):
            try:
                print Y_value
                img.crop((X_value[i], Y_value[0], X_value[i + 1], Y_value[(len(Y_value) - 1)] + 1)).save(
                    "/home/tongtong/pic_codec/TrainNum/%d%d.jpg" % (i / 2, img_len))
            except:
                Image.open(ur"/home/tongtong/pic_codec/TrainNum/%d.jpg" % (i / 2))


    # ---------------------------------------------------------------------------------------------
    # 图片识别

    def get_feature(self, img):
        """
        获取指定图片的特征值,
        1. 按照每排的像素点,高度为10,则有10个维度,然后为7列,总共16个维度
        :param img_path:
        :return:一个维度为10（高度）的列表
        """

        width, height = img.size

        print img.size

        pixel_cnt_list = []
        # height = 10
        for y in range(height):
            pix_cnt_x = 0
            for x in range(width):
                rgb_value = img.getpixel((x, y))
                r, g, b = rgb_value[0], rgb_value[1], rgb_value[2]
                if r == 0 and g == 0 and b == 0:
                    pix_cnt_x += 1

            pixel_cnt_list.append(pix_cnt_x)

        for x in range(width):
            pix_cnt_y = 0
            for y in range(height):
                rgb_value = img.getpixel((x, y))
                r, g, b = rgb_value[0], rgb_value[1], rgb_value[2]
                if r == 0 and g == 0 and b == 0:  # 黑色点
                    pix_cnt_y += 1

            pixel_cnt_list.append(pix_cnt_y)

        return pixel_cnt_list

    def Write_LibSvmData(self, modeNum, imageDir):
        '''
        按照 libSVM 指定的格式生成一组带特征值和标记值的向量文件
        :param modeNum:
        :param imageDir:
        :return:
        '''
        f = open('/home/tongtong/pic_codec/mode/data' + '.txt', 'ar+')
        f.truncate()
        for j in range(modeNum):
            for modeImageList in os.listdir(imageDir + str(j)):
                if modeImageList.endswith('jpg'):
                    feature_list = self.get_feature(
                        Image.open('/home/tongtong/pic_codec/mode/' + str(j) + '/' + modeImageList))

                    s = str(j)
                    for index in range(len(feature_list)):
                        s += ' ' + str(index) + ':' + str(feature_list[index])
                    s += '\n'
                    f.write(s)
        f.close()

    def Write_testteLibSvmData(self, modeNum, imageDir):
        f = open(imageDir + 'data.txt', 'ar+')
        f.truncate()
        for j in range(modeNum):
            for modeImageList in os.listdir(imageDir + str(j)):
                if modeImageList.endswith('jpg'):
                    feature_list = self.get_feature(
                        Image.open(imageDir + str(j) + '/' + modeImageList))

                    s = str(j)
                    for index in range(len(feature_list)):
                        s += ' ' + str(index) + ':' + str(feature_list[index])
                    s += '\n'
                    f.write(s)
        f.close()

    def train_svm_model(self, Train_path, Test_root):
        """
        训练并生成model文件
        :return:
        """
        y, x = svm_read_problem(Train_path + 'data.txt')
        yt, xt = svm_read_problem(Test_root + 'data.txt')
        model = svm_train(y, x)
        #svm_save_model(model_path, model)
        p_label, p_acc, p_val = svm_predict(yt, xt, model)  # p_label即为识别的结果
        print p_label
        print p_acc
        print p_val


TrainSet().binary('/home/tongtong/codectest/', '/home/tongtong/pic_codec/TrainImage/')
#TrainSet().Write_testteLibSvmData(10, '/home/tongtong/pic_codec/testmode/')

TrainSet().train_svm_model('/home/tongtong/pic_codec/mode/', '/home/tongtong/pic_codec/testmode/')
