import random

from ContinuousSignal import ContinuousSignal


class UniformNoise(ContinuousSignal):
    def __init__(self, A, T, t1, d, f, bins=None):
        super().__init__(A, t1, d, f, bins)
        self.T = T

    def calculate_data(self, t):
        return random.uniform(0, 1) * (2 * self.A) - self.A
