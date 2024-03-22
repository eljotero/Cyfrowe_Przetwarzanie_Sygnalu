import struct
import numpy as np
from matplotlib import pyplot as plt


class SignalGenerator:
    def __init__(self, A, t1, d, f, bins=None, type=None):
        self.A = A
        self.t1 = t1
        self.d = d
        self.f = f
        self.data = []
        self.indexes = []
        self.avg_value = None
        self.abs_avg_value = None
        self.avg_power = None
        self.variance = None
        self.effect_value = None
        if bins is None:
            self.bins = 10
        elif bins in [5, 10, 15, 20]:
            self.bins = bins
        else:
            available_bins = [5, 10, 15, 20]
            available_values = np.array([5, 10, 15, 20])
            self.bins = int(np.interp(bins, available_bins, available_values))
        if type is None:
            self.type = "float"
        else:
            self.type = type

    def generate_data(self):
        for i in range(self.d * self.f):
            t = self.t1 + i / self.f
            self.data.append(self.calculate_data(t))
            self.indexes.append(t)
        return self.calculate_values(), self.generate_chart(), self.generate_bar_chart()

    def calculate_data(self, t):
        raise NotImplementedError("Metoda calculate_data() musi być zaimplementowana w klasie potomnej.")

    def calculate_values(self):
        raise NotImplementedError("Metoda calculate_values() musi być zaimplementowana w klasie potomnej.")

    def generate_chart(self):
        plt.clf()
        plt.plot(self.indexes, self.data)
        plt.savefig('chart.png')
        return plt

    def generate_bar_chart(self):
        plt.clf()
        plt.hist(self.data, bins=self.bins)
        plt.savefig('histogram.png')
        return plt

    def save_to_binary_file(self, filename):
        with open(filename, 'wb') as file:
            file.write(struct.pack('<d', self.t1))
            file.write(struct.pack('<d', self.f))
            if self.type == "complex":
                file.write(struct.pack('<i', 1))
            else:
                file.write(struct.pack('<i', 0))
            file.write(struct.pack('<i', len(self.data)))
            for value in self.data:
                file.write(struct.pack('<d', value))
