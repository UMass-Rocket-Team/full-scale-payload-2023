from collections import deque
from statistics import mean, variance

class RocketQueue(deque):
    def __init__(self,max_len=None, threshold=None):
        super().__init__(maxlen=max_len)
        self.threshold = threshold
        self.count = 0
    
    def enqueue(self, item):
        super().append(item)
        if self.threshold != None and item > self.threshold:
            self.count += 1
    
    def dequeue(self):
        item = super().popleft()
        if self.threshold != None and item > self.threshold:
            self.count -= 1
        return item
    def size(self):
        return len(self)
    def num_greater_than_threshold(self):
        return self.count
    
    def get_proportion_above_threshold(self):
        if self.size() == 0:
            return 0
        return self.num_greater_than_threshold() / self.size()
    
    def get_mean(self):
        if self.size() == 0:
            return None
        return mean(self)
    
    def get_variance(self):
        if self.size() == 0:
            return None
        return variance(self)
    def peek(self):
        if self.size() == 0:
            print("Queue is empty")
            return None
        return self[0]
    
