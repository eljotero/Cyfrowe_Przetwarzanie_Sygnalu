import math
import random

from ContinuousSignal import ContinuousSignal


class GaussianNoise(ContinuousSignal):

    def __init__(self, A, t1, d, f, bins=None, signal_type=None):
        super().__init__(A, t1, d, f, bins, signal_type)

    def calculate_data(self, t):
        return self.A * math.pow(math.sqrt(2 * math.pi) * math.e, -math.pow(random.uniform(0, 1), 2) / 2)
