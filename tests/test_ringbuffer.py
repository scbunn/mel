import unittest
from app.RingBuffer import RingBuffer


class RingBufferTestCase(unittest.TestCase):
    def setUp(self):
        self.rb = RingBuffer(500000)

    def test_ringbuffer_inital_size(self):
        self.assertTrue(self.rb.get_size() == 0)

    def test_ringbuffer_append(self):
        for i in range(0, 10000):
            self.rb.append(i)
        self.assertTrue(self.rb.get_size() == 10000)

    def test_ringbuffer_overflow(self):
        for i in range(0, 1000000):
            self.rb.append(i)
        self.assertTrue(self.rb.get_size() == 500000)

    def test_ringbuffer_iteration(self):
        count = 0
        for item in self.rb:
            count += 1
        self.assertTrue(count == self.rb.get_size())

    def test_ringbuffer_pop(self):
        size = self.rb.get_size()
        iterations = 0
        while (self.rb.get_size() != 0):
            self.rb.pop()
            iterations += 1
        self.assertTrue(size == iterations)
        self.assertTrue(self.rb.get_size() == 0)
