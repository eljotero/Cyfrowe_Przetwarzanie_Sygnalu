import numpy as np
from matplotlib import pyplot as plt

from Discrete.DiscreteSignal import DiscreteSignal


class ImpulseNoise(DiscreteSignal):
    def __init__(self, A, t1, d, f, p, bins=None, signal_type=None, id=None):
        super().__init__(A, t1, d, f, bins, signal_type, id)
        self.A = A
        self.t1 = t1
        self.d = d
        self.f = f
        self.p = p / 100

    def generate_data(self):
        for i in range(int(self.d * self.f)):
            t = self.t1 + i / self.f
            self.data.append(self.calculate_data(t))
            self.indexes.append(t)
        return self.calculate_values(), self.generate_chart(), self.generate_bar_chart()

    def calculate_data(self, t):
        if self.p > np.random.rand():
            return self.A
        else:
            return 0

    def calculate_values(self):
        super().calculate_values()

    def generate_chart(self):
        plt.clf()
        plt.scatter(self.indexes, self.data)
        plt.savefig('chart.png')
        return plt

    def generate_bar_chart(self):
        plt.clf()
        plt.hist(self.data, bins=self.bins)
        plt.savefig('histogram.png')
        return plt
