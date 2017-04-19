#!/usr/bin/python
# -*- coding: UTF-8 -*-s

'''
单链表实现
链表首部插入
链表首部删除
链表尾部插入
链表尾部删除
任意位置插入
任意位置删除
清除链表
获取链表大小
打印链表
查询任意数据项
'''
import Node
from Log import log

class myArray(object):

    def __init__(self):
        self.head = None
        self.theSize = 0

    def clear(self):
        self.__doClear()

    def __doClear(self):
        if self.head is None:
            return
        self.head = None
        self.theSize = 0

    def isEmpty(self):
        if self.head is None:
            return True
        return False

    def size(self):
        return self.theSize

    def __doAppendFirst(self, insertedNode):
        nextNode = self.head
        self.head = insertedNode
        self.head._next = nextNode

    def appendFirst(self, item):
        if item is None:
            return
        self.theSize = self.theSize + 1
        insertedNode = Node.nodeStructure(item)
        if self.isEmpty():
            self.head = insertedNode
        else:
            self.__doAppendFirst(insertedNode)

    def __doAppendLast(self, insertedNode):
        preNode = self.head
        while (preNode._next is not None):
            preNode = preNode._next
        preNode._next = insertedNode

    def appendLast(self, item):
        if item is None:
            return
        self.theSize = self.theSize + 1
        insertedNode = Node.nodeStructure(item)
        if self.isEmpty():
            self.head = insertedNode
            return
        self.__doAppendLast(insertedNode)

    def __isOperate(self, index):
        if self.isEmpty():
            print 'List is Empty'
            return False
        if index < 0 or index > self.size():
            print 'Index Out'
            return False
        return True

    def insert(self, index, item):
        if self.__isOperate(index):
            if index is 0:
                self.appendFirst(item)
            elif index is self.size():
                self.appendLast(item)
            preNodeOfOperatedNode, nextNodeOfOperatedNode = self.__doGet_Pre_Next(index)
            preNodeOfOperatedNode._next = Node.nodeStructure(item)
            preNodeOfOperatedNode._next._next = nextNodeOfOperatedNode

    def deleteLastNode(self):
        nextNode = self.head
        while(nextNode._next._next is not None):
            nextNode = nextNode._next
        self.theSize = self.theSize -1
        nextNode._next = None

    def deleteFirstNode(self):
        print 'firestNode'
        self.theSize = self.theSize - 1
        self.head = self.head._next

    def remove(self, index):
        if self.__isOperate(index):
            print ('remove')
            if index is 0:
                self.deleteFirstNode()
            elif index is self.size()-1:
                self.deleteLastNode()
            else:
                self.theSize = self.theSize -1
                preNodeOfOperatedNode, nextNodeOfOperatedNode = self.__doGet_Pre_Next(index)
                preNodeOfOperatedNode._next = nextNodeOfOperatedNode._next

    def __doGet_Pre_Next(self, index):
        i = 0
        nextNodeOfOperatedNode = self.head
        preNodeOfOperatedNode = self.head
        while (i < index and nextNodeOfOperatedNode._next is not None):
            preNodeOfOperatedNode = nextNodeOfOperatedNode
            nextNodeOfOperatedNode = nextNodeOfOperatedNode._next
            i = i + 1
        return preNodeOfOperatedNode, nextNodeOfOperatedNode

    def __doGet(self, index):
        i = 0
        currentNode = self.head
        while (i < index):
            currentNode = currentNode._next
            i = i + 1
        return currentNode


    def get(self, index):
        log().logBeforeMethod("get(self, index)")
        if self.__isOperate(index):
            return self.__doGet(index)
        return "Non-existent Node"

    def printArrayList(self):
        log().logBeforeMethod("printArrayList(self)")
        currentNode = self.head
        count = 0
        while(count < self.theSize):
            print currentNode.element
            currentNode = currentNode._next
            count = count +1


testArray = myArray()
testArray.appendFirst(12)
print(testArray.size())
testArray.appendFirst(19)
testArray.appendFirst(13)
testArray.printArrayList()
print(testArray.size())
testArray.remove(7)
testArray.remove(2)
print(testArray.size())
testArray.clear()
print (testArray.size())
print (testArray.get(0))
