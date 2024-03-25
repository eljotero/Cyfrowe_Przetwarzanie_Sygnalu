import math

from ContinuousSignal import ContinuousSignal


class TriangularWave(ContinuousSignal):
    def __init__(self, A, T, t1, d, kw, f, bins=None, signal_type=None):
        super().__init__(A, t1, d, f, bins, signal_type)
        self.kw = kw
        self.T = T

    def calculate_data(self, t):
        k = ((t - self.t1) / self.T) - math.floor((t - self.t1) / self.T)
        if k < self.kw:
            return k / self.kw * self.A
        else:
            return (1 - (k - self.kw) / (1 - self.kw)) * self.A
