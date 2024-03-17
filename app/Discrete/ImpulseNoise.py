import numpy as np
from matplotlib import pyplot as plt

from DiscreteSignal import DiscreteSignal


class ImpulseNoise(DiscreteSignal):
    def __init__(self, A, t1, d, f, p, bins=None, signal_type=None):
        super().__init__(A, t1, d, f, bins, signal_type)
        self.A = A
        self.t1 = t1
        self.d = d
        self.f = f
        self.p = p / 100

    def calculate_data(self, t):
        if self.p > np.random.rand():
            return self.A
        else:
            return 0

    def calculate_values(self):
        super().calculate_values()

    def generate_chart(self):
        plt.scatter(self.indexes, self.data)
        plt.show()
