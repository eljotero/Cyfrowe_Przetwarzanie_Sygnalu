import math
from Continuous.ContinuousSignal import ContinuousSignal


class FullWave(ContinuousSignal):
    def __init__(self, A, T, t1, d, f, bins=None, signal_type=None, id=None):
        super().__init__(A, t1, d, f, bins, signal_type, id)
        self.T = T

    def calculate_data(self, t):
        return self.A * abs(math.sin(((2 * math.pi) / self.T) * (t - self.t1)))
