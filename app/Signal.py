import struct

import numpy as np
from matplotlib import pyplot as plt


class Signal:
    def __init__(self, t1, f, data, indexes, type=None):
        self.t1 = t1
        self.f = f
        if type is None:
            self.type = "float"
        else:
            self.type = type
        self.data = data
        self.indexes = indexes

    @staticmethod
    def load_from_binary_file(filename):
        with open(filename, 'rb') as file:
            t1 = struct.unpack('<d', file.read(8))[0]
            f = struct.unpack('<d', file.read(8))[0]
            type_value = struct.unpack('<i', file.read(4))[0]
            if type_value == 1:
                type = "complex"
            else:
                type = "float"
            num_samples = struct.unpack('<i', file.read(4))[0]
            data = [struct.unpack('<d', file.read(8))[0] for _ in range(num_samples)]
            indexes = np.array([t1 + i / f for i in range(len(data))])
            return Signal(t1, f, data, indexes, type)

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

    def add(self, second_signal):
        if len(self.data) != len(second_signal.data):
            raise ValueError("Dlugosci sygnalow nie są rowne.")
        data = [a + b for a, b in zip(self.data, second_signal.data)]
        indexes = np.array([self.t1 + i / self.f for i in range(len(data))])
        result_singal = Signal(self.t1, self.f, data, indexes)
        return result_singal

    def subtract(self, second_signal):
        if len(self.data) != len(second_signal.data):
            raise ValueError("Dlugosci sygnalow nie są rowne.")
        data = [a - b for a, b in zip(self.data, second_signal.data)]
        indexes = np.array([self.t1 + i / self.f for i in range(len(data))])
        result_signal = Signal(self.t1, self.f, data, indexes)
        return result_signal

    def multiply(self, second_signal):
        if len(self.data) != len(second_signal.data):
            raise ValueError("Dlugosci sygnalow nie są rowne.")
        data = [a * b for a, b in zip(self.data, second_signal.data)]
        indexes = np.array([self.t1 + i / self.f for i in range(len(data))])
        result_signal = Signal(self.t1, self.f, data, indexes)
        return result_signal

    def divide(self, second_signal):
        if len(self.data) != len(second_signal.data):
            raise ValueError("Dlugosci sygnalow nie są rowne.")
        data = [a / b if b != 0 else 0 for a, b in zip(self.data, second_signal.data)]
        indexes = np.array([self.t1 + i / self.f for i in range(len(data))])
        result_signal = Signal(self.t1, self.f, data, indexes)
        return result_signal

    def generate_data(self):
        return None, self.generate_chart(), self.generate_bar_chart()

    def generate_chart(self):
        plt.clf()
        plt.plot(self.indexes, self.data)
        plt.savefig('chart.png')
        return plt

    def generate_bar_chart(self):
        plt.clf()
        plt.hist(self.data, bins=10, rwidth=0.9)
        plt.savefig('histogram.png')
        return plt
