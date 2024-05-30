import numpy as np

from Continuous.ContinuousSignal import ContinuousSignal


class GaussianNoise(ContinuousSignal):

    def __init__(self, A, t1, d, f, bins=None, signal_type=None, id=None):
        super().__init__(A, t1, d, f, bins, signal_type, id)

    def calculate_data(self, t):
        return self.A * np.random.normal(0, 1)
