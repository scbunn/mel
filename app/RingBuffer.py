from collections import deque
import random


class RingBuffer(deque):
    """An in memory implementation of a ring buffer"""

    def __init__(self, size=1024):
        deque.__init__(self, maxlen=size)
        self._size = size

    def append(self, data):
        """Add a data element to the end of the buffer"""
        deque.append(self, data)

    def pop(self):
        """Return an element from the left of the buffer"""
        return self.popleft()

    def to_list(self):
        """Return all current elements in buffer as a list"""
        return list(self)

    def get_size(self):
        """Return the number of elements in the buffer"""
        return len(self.to_list())


if __name__ == "__main__":
    """Test the ring buffer implementation"""
    rb = RingBuffer(25)
    print("rb size: {}".format(rb.get_size()))

    for i in range(100000):
        elem = {}
        elem['id'] = i
        elem['data'] = random.randint(1, 3000)
        rb.append(elem)

    print("rb size: {}".format(rb.get_size()))

    for i in rb:
        print("element id: {}\t\tdata: {}".format(i['id'], i['data']))

    print("rb size: {}".format(rb.get_size()))
    print(rb.to_list())

    print(rb.pop())
    print("rb size: {}".format(rb.get_size()))
