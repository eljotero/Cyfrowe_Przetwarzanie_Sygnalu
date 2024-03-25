import numpy as np
from SignalGenerator import SignalGenerator


class ContinuousSignal(SignalGenerator):
    def __init__(self, A, t1, d, f, bins=None, signal_type=None):
        super().__init__(A, t1, d, f, bins, signal_type)

    def calculate_values(self):
        self.avg_value = 1 / (self.indexes[-1] - self.indexes[0]) * np.trapz(self.data, self.indexes)
        self.abs_avg_value = 1 / (self.indexes[-1] - self.indexes[0]) * np.trapz(np.abs(self.data), self.indexes)
        self.avg_power = 1 / (self.indexes[-1] - self.indexes[0]) * np.trapz(np.power(self.data, 2), self.indexes)
        self.variance = 1 / (self.indexes[-1] - self.indexes[0]) * np.trapz(np.power(self.data - self.avg_value, 2),
                                                                            self.indexes)
        self.effect_value = np.sqrt(self.avg_power)
        return self.avg_value, self.abs_avg_value, self.avg_power, self.variance, self.effect_value
