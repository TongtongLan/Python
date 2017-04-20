#!/usr/bin/python
# -*- coding: UTF-8 -*-s
'''
实现一个双端链表
结点插入（任意位置插入、链表表头插入、链表表尾插入）
遍历打印链表数据项
根据索引查询数据项

删除
'''

import Node
import Log


class doubleEndedList_Node(Node.nodeStructure):
    def __init__(self, element):
        super(doubleEndedList_Node, self).__init__(element)
        self.last = None

class doubleEndedList:
    def __init__(self):
        self.__doClear()

    def clear(self):
        Log.log().logBeforeMethod("clear(self)")
        self.__doClear()

    def __doClear(self):
        self.theSize = 0
        self.head = doubleEndedList_Node(None)
        self.head.last = self.head

    def __packageNode(self, element):
        return doubleEndedList_Node(element)

    def __doInsert(self, index, insertedElement):
        if index is 0:
            self.insertFirstNode(insertedElement)
        elif index is self.theSize:
            self.insertLastNode(insertedElement)
        else:
            self.__insertMiddleNode(index, insertedElement)

    def __insertInEmptyList(self, newNode):
        self.head = newNode
        self.head.last = self.head
        self.theSize = self.auto_Increment(self.theSize)

    def __insertInNotEmptyList(self, newNode):
        nextNode = self.head
        self.head = newNode
        self.head._next = nextNode
        self.head.last = nextNode.last
        self.theSize = self.auto_Increment(self.theSize)

    def __insertMiddleNode(self, index, element):
        self.theSize = self.auto_Increment(self.theSize)
        insertedNode = doubleEndedList_Node(element)
        beforeInsertedNode = self.findNodeByIndex(self.auto_Decrement(index))
        insertedNode._next = beforeInsertedNode._next
        beforeInsertedNode._next = insertedNode

    def __doPrintList(self):
        currentNode = self.head
        count = 0
        while (currentNode is not None and count < self.theSize):
            print (currentNode.element)
            currentNode = currentNode._next
            count = self.auto_Increment(count)

    def auto_Increment(self, variable):
        return variable + 1

    def auto_Decrement(self, variable):
        return variable - 1

    def isEmpty(self):
        if self.theSize is 0:
            return True
        return False

    def insertFirstNode(self, insertetElement):
        Log.log().logBeforeMethod("insertFirstNode(self, insertetElement)")
        if self.isEmpty():
            self.__insertInEmptyList(self.__packageNode(insertetElement))
        else:
            self.__insertInNotEmptyList(self.__packageNode(insertetElement))

    def insertLastNode(self, element):
        pass

    def findNodeByIndex(self, index):
        currentNode = self.head
        count = 1
        while (count < index):
            currentNode = currentNode._next
            count = self.auto_Increment(count)
        return currentNode

    def isIndexOut(self, index):
        if index < 0 or index > self.theSize:
            print ("Array out error")
            return True
        return False

    def insert(self, index, insertedElement):
        if self.isIndexOut(index):
            print ("Array out error")
        else:
            self.__doInsert(index, insertedElement)

    def printList(self):
        Log.log().logBeforeMethod("printList(self)")
        if self.isEmpty():
            print "The List is NULL"
        else:
            self.__doPrintList()

    def printLastNode(self):
        Log.log().logBeforeMethod("printLastNode(self)")
        if self.head.last is None:
            print (self.head.element)
            return
        print ("print last node")
        print (self.head.last.element)

    def contain(self, element):
        Log.log().logBeforeMethod("contain(self, element)")
        if self.isEmpty():
            return False
        elif self.findWithElement(element) is not None:
            return True
        else:
            return False

    def findWithElement(self, element):
        Log.log().logBeforeMethod("findWithElement(self, element)")
        currentNode = self.head
        while(currentNode is not None):
            if currentNode.element is element:
                return currentNode
            currentNode = currentNode._next





testDoubleEndedList = doubleEndedList()
print (testDoubleEndedList.theSize)
print (testDoubleEndedList.isEmpty())
testDoubleEndedList.insertFirstNode(123)
testDoubleEndedList.printLastNode()
testDoubleEndedList.insertFirstNode(345)
print (testDoubleEndedList.theSize)
testDoubleEndedList.printList()
testDoubleEndedList.insert(1, 678)
testDoubleEndedList.printList()
testDoubleEndedList.insert(2, 3623)
testDoubleEndedList.printList()
testDoubleEndedList.insert(1, 467)
print (testDoubleEndedList.findWithElement(23))
print (testDoubleEndedList.findWithElement(467))
print (testDoubleEndedList.contain(11))
print (testDoubleEndedList.contain(467))

print (testDoubleEndedList.theSize)
testDoubleEndedList.printLastNode()
testDoubleEndedList.printList()
testDoubleEndedList.clear()
testDoubleEndedList.printList()


