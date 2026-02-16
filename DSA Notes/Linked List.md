# Linked List

The structure of an unordered list, as described above, is a collection of items where each item holds a relative position with respect to the others. Some possible unordered list operations are given below.

### Operations

​

`List()` creates a new list that is empty. It needs no parameters and returns an empty list.

`add(item)` adds a new item to the list. It needs the item and returns nothing. Assume the item is not already in the list.

`remove(item)` removes the item from the list. It needs the item and modifies the list. Assume the item is present in the list.

`search(item)` searches for the item in the list. It needs the item and returns a boolean value.

`isEmpty()` tests to see whether the list is empty. It needs no parameters and returns a boolean value.

`size()` returns the number of items in the list. It needs no parameters and returns an integer.

`append(item)` adds a new item to the end of the list making it the last item in the collection. It needs the item and returns nothing. Assume the item is not already in the list.

`index(item)` returns the position of item in the list. It needs the item and returns the index. Assume the item is in the list.

`insert(pos,item)` adds a new item to the list at position pos. It needs the item and returns nothing. Assume the item is not already in the list and there are enough existing items to have position pos.

`pop()` removes and returns the last item in the list. It needs nothing and returns an item. Assume the list has at least one item.

`pop(pos)` removes and returns the item at position pos. It needs the position and returns the item. Assume the item is in the list.

# Implementation

### Node Class

The basic building block for the linked list implementation is the **node**. Each node object must hold at least two pieces of information. First, the node must contain the list item itself. We will call this the **data field** of the node. In addition, each node must hold a reference to the next node

```python

class Node:
    def __init__(self,initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self,newdata):
        self.data = newdata

    def setNext(self,newnext):
        self.next = newnext

```

### List Class

As we suggested above, the unordered list will be built from a collection of nodes, each linked to the next by explicit references. As long as we know where to find the first node (containing the first item), each item after that can be found by successively following the next links. With this in mind, the `UnorderedList` class must maintain a reference to the first nod

```python
class UnorderedList:
    def __init__(self):
        self.head = None
        
    def add(self,item):
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp
```

### Operations

#### Add

```python
def add(self,item):
    temp = Node(item)
    temp.setNext(self.head)
    self.head = temp
```

#### Size
```python
def size(self):
    current = self.head
    count = 0
    while current != None:
        count = count + 1
        current = current.getNext()

    return count
```

#### Search
```python
def search(self,item):
    current = self.head
    found = False
    while current != None and not found:
        if current.getData() == item:
            found = True
        else:
            current = current.getNext()

    return found
```

#### Remove

In order to remove the node containing the item, we need to modify the link in the previous node so that it refers to the node that comes after `current`. Unfortunately, there is no way to go backward in the linked list. Since `current` refers to the node ahead of the node where we would like to make the change, it is too late to make the necessary modification.

The solution to this dilemma is to use two external references as we traverse down the linked list. `current` will behave just as it did before, marking the current location of the traverse. The new reference, which we will call `previous`, will always travel one node behind `current`. That way, when `current` stops at the node to be removed, `previous` will be referring to the proper place in the linked list for the modification

![Initial Values for the `previous` and `current` Reference](linkedlist1.png)

![`previous` and `current` Move Down the List](linkedlist2.png)

![[linkedlist3.png|Removing an Item from the Middle of the Lis]]

![[linkedlist4.png|Removing the First Node from the List]]



```python
def remove(self,item):
    current = self.head
    previous = None
    found = False
    while not found:
        if current.getData() == item:
            found = True
        else:
            previous = current
            current = current.getNext()

    if previous == None:
        self.head = current.getNext()
    else:
        previous.setNext(current.getNext())

```