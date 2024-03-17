from ContinuousSignal import ContinuousSignal


class TriangularWave(ContinuousSignal):
    def __init__(self, A, T, t1, d, kw, f, bins=None, signal_type=None):
        super().__init__(A, t1, d, f, bins, signal_type)
        self.kw = kw
        self.T = T

    def calculate_data(self, t):
        if (t - self.t1) % self.T < self.kw:
            return (2 * self.A / self.kw) * t - self.A
        else:
            return (-2 * self.A / (self.T - self.kw)) * t + 3 * self.A

