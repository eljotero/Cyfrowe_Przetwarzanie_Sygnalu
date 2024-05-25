import math

from ContinuousSignal import ContinuousSignal


class SquareWave(ContinuousSignal):
    def __init__(self, A, T, t1, d, f, kw, bins=None, signal_type=None, id=None):
        super().__init__(A, t1, d, f, bins, signal_type, id)
        self.T = T
        self.kw = kw

    def calculate_data(self, t):
        k = math.floor((t - self.t1) / self.T)
        if k * self.T + self.t1 <= t < self.kw * self.T + k * self.T + self.t1:
            return self.A
        elif self.kw * self.T - k * self.T + self.t1 <= t < self.T + k * self.T + self.t1:
            return 0
