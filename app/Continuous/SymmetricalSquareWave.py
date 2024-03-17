from ContinuousSignal import ContinuousSignal


class SymmetricalSquareWave(ContinuousSignal):
    def __init__(self, A, T, t1, d, f, kw, bins=None):
        super().__init__(A, t1, d, f, bins)
        self.T = T
        self.kw = kw

    def calculate_data(self, t):
        if (t - self.t1) % self.T < self.kw:
            return self.A
        else:
            return -self.A
