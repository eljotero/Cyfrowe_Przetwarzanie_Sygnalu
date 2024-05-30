from Continuous.ContinuousSignal import ContinuousSignal


class UnitStep(ContinuousSignal):
    def __init__(self, A, t1, d, ts, f, bins=None, signal_type=None, id=None):
        super().__init__(A, t1, d, f, bins, signal_type, id)
        self.ts = ts

    def calculate_data(self, t):
        if t < self.ts:
            return 0
        elif t == self.ts:
            return self.A / 2
        else:
            return self.A
