import math

from ContinuousSignal import ContinuousSignal


class TriangularWave(ContinuousSignal):
    def __init__(self, A, T, t1, d, kw, f, bins=None, signal_type=None):
        super().__init__(A, t1, d, f, bins, signal_type)
        self.kw = kw
        self.T = T

    def calculate_data(self, t):
        k = math.floor((t - self.t1) / self.T)
        if k * self.T + self.t1 <= t < self.kw * self.T + k * self.T + self.t1:
            return (self.A / (self.kw * self.T)) * (t - (k * self.T) - self.t1)
        elif self.kw * self.T + self.t1 + k * self.T <= t < self.T + k * self.T + self.t1:
            return (-self.A / (self.T * (1 - self.kw))) * (t - (k * self.T) - self.t1)
        else:
            return 0
