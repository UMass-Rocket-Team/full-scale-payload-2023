import time
from singleton import Singleton
class RocketTimer(metaclass=Singleton):
    def __init__(self):
        print("RocketTimer init")#DEBUG
        self.start_time = time.monotonic_ns() / 1_000_000
    def time_since_init_ms (self):
        return (time.monotonic_ns() / 1_000_000) - self.start_time
    @staticmethod
    def time_since_ms(time_ms):
        return (time.monotonic_ns() / 1_000_000) - time_ms
    @staticmethod
    def time_diff (final_time, init_time):
        return (final_time - init_time)
    @staticmethod
    def get_time_ms ():
        return time.monotonic_ns() / 1_000_000


