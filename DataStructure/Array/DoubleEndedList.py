import Node
import Log

class doubleEndedList_Node(Node.nodeStructure):
    def __init__(self, element):
        super(doubleEndedList_Node, self).__init__(element)
        self.last = None

class doubleEndedList:
    def __init__(self):
        self.doClear()

    def clear(self):
        Log.log().logBeforeMethod("clear(self)")
        self.doClear()

    def doClear(self):
        self.theSize = 0
        self.head = doubleEndedList_Node(None)
        self.head.last = self.head

    def isEmpty(self):
        if self.theSize is 0:
            return True
        return False

    def insertFirstNode(self, insertetElement):
        Log.log().logBeforeMethod("insertFirstNode(self, insertetElement)")
        newHead = doubleEndedList_Node(insertetElement)
        if self.isEmpty():
            print ("insert"+str(insertetElement))
            self.head = newHead
            self.head.last = self.head
            self.theSize = self.theSize + 1
        else:
            print ("insert" + str(insertetElement))
            nextNode = self.head
            self.head = newHead
            self.head._next = nextNode
            self.head.last = nextNode.last
            self.theSize = self.theSize + 1


    def insertLastNode(self, element):
        pass

    def insert(self, index, insertetElement):
        if index < 0 or index > self.theSize:
            print ("Array out error")
            return
        if index is 0:
            self.insertFirstNode(insertetElement)
        elif index is self.theSize:
            self.insertLastNode(insertetElement)
        else:
            self.theSize = self.theSize + 1
            currentNode = self.head
            count = 1
            while(count < index):
                currentNode = currentNode._next
                count = count + 1
            insertedNode = doubleEndedList_Node(insertetElement)
            insertedNode._next = currentNode._next
            currentNode._next = insertedNode

    def printList(self):
        Log.log().logBeforeMethod("printList(self)")
        if self.isEmpty():
            print "The List is NULL"
            return
        currentNode = self.head
        count = 0
        while(currentNode is not None and count < self.theSize):
            print (currentNode.element)
            currentNode = currentNode._next
            count = count + 1

    def printLastNode(self):
        Log.log().logBeforeMethod("printLastNode(self)")
        if self.head.last is None:
            print (self.head.element)
            return
        print ("print last node")
        print (self.head.last.element)



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
print (testDoubleEndedList.theSize)
testDoubleEndedList.printLastNode()
testDoubleEndedList.printList()
testDoubleEndedList.clear()
testDoubleEndedList.printList()

