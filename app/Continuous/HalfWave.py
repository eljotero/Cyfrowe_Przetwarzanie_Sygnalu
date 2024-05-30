import math

from Continuous.ContinuousSignal import ContinuousSignal


class HalfWave(ContinuousSignal):
    def __init__(self, A, T, t1, d, f, bins=None, signal_type=None, id=None):
        super().__init__(A, t1, d, f, bins, signal_type, id)
        self.T = T

    def calculate_data(self, t):
        return 0.5 * self.A * (math.sin((2 * math.pi / self.T) * (t - self.t1)) + abs(
            math.sin((2 * math.pi / self.T) * (t - self.t1))))

