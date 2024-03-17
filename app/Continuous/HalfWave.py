import math

from ContinuousSignal import ContinuousSignal


class HalfWave(ContinuousSignal):
    def __init__(self, A, T, t1, d, f, bins=None):
        super().__init__(A, t1, d, f, bins)
        self.T = T

    def calculate_data(self, t):
        return 0.5 * self.A * (math.sin((2 * math.pi / self.T) * (t - self.t1)) + abs(
            math.sin((2 * math.pi / self.T) * (t - self.t1))))

