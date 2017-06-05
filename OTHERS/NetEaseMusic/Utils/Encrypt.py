#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import base64
from Crypto.Cipher import AES


class Encrypt():

    '''
    分析neteaseCloudMusic JS 可知加密方式为AES.MODE_CBC加密,
    模拟加密方式获得params和encSecKey参数
    '''

    BS = 16
    AES_MODE = AES.MODE_CBC

    def __init__(self):
        pass

    def aesEncrypt(self, text, secKey):
        '''
        AES加密test, 两次调用以获得params
        CBC模式
        :param text: 需要加密的数据
        :param secKey:
        :return:
        '''
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, self.AES_MODE, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def rsaEncrypt(self, secKey, pubKey, modulus):
        '''
        加密获得encSecKey
        :param secKey:
        :param pubKey:
        :param modulus:
        :return: encSecKey
        '''
        text = secKey[::-1]
        rs = int(text.encode('hex'), self.BS) ** int(pubKey, self.BS) % int(modulus, self.BS)
        return format(rs, 'x').zfill(256)

    def createSecretKey(self, size):
        '''
        生成size大小的随机数
        :param size:
        :return: 长度为size的随机数
        '''
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]
