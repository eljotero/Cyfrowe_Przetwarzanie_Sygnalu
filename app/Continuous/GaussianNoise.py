import numpy as np

from ContinuousSignal import ContinuousSignal


class GaussianNoise(ContinuousSignal):

    def __init__(self, A, t1, d, f, bins=None, signal_type=None):
        super().__init__(A, t1, d, f, bins, signal_type)

    def calculate_data(self, t):
        return self.A * np.random.normal(0, 1)
