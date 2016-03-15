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


class MarathonEventBuffer(object):
    """Class to manage marathon events in the buffer"""

    def __init__(self, buffer_size=1024):
        self.buffer = RingBuffer(buffer_size)

    def get_size(self):
        """Return the number of events buffered"""
        return self.buffer.get_size()

    def add_event(self, event):
        self.buffer.append(event)

    def get_summary_events(self):
        """Return a summary of all buffered events"""
        events = []
        for event in self.buffer:
            item = {}
            item['id'] = event.id
            item['timestamp'] = event.timestamp
            item['eventType'] = event.eventType
            item['marathon_host'] = event.marathon_host
            item['url'] = event.get_url()
            item['processed'] = event.isProcessed()
            events.append(item)

        return events

    def get_events(self):
        """Return all buffered events"""
        return self.buffer.to_list()


if __name__ == "__main__":
    """Test the ring buffer implementation"""
    import datetime

    eb = MarathonEventBuffer(25)
    print("eb size: {}".format(eb.get_size()))

    for i in range(100000):
        elem = {}
        elem['id'] = i
        elem['data'] = random.randint(1, 3000)
        elem['timestamp'] = datetime.datetime.utcnow().isoformat()
        elem['eventType'] = 'test event'
        elem['marathon_host'] = '127.0.0.1'
        elem['marathon_event'] = {
            'message': 'not part of the summary',
            'field1': 'value 2'
        }
        eb.add_event(elem)

    print("eb size: {}".format(eb.get_size()))
    for i in eb.get_events():
        print(i)

    print("event summary:")
    for event in eb.get_summary_events():
        print(event)

    print("events:")
    for event in eb.get_events():
        print(event)
