import numpy as np
from matplotlib import pyplot as plt


class SignalGenerator:
    def __init__(self, A, t1, d, f, bins=None):
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

    def add(self, second_signal):
        if len(self.data) != len(second_signal.data):
            raise ValueError("Dlugosci sygnalow nie są rowne.")
        result_signal = SignalGenerator(A=0, t1=self.t1, d=self.d, f=self.f, bins=self.bins)
        for i in range(len(self.data)):
            result_signal.data.append(self.data[i] + second_signal.data[i])
        result_signal.generate_bar_chart()
        result_signal.generate_chart()
        return result_signal

    def subtract(self, second_signal):
        if len(self.data) != len(second_signal.data):
            raise ValueError("Dlugosci sygnalow nie są rowne.")
        for i in range(len(self.data)):
            self.data[i] -= second_signal.data[i]
        return self.generate_bar_chart(), self.generate_chart()

    def multiply(self, second_signal):
        if len(self.data) != len(second_signal.data):
            raise ValueError("Dlugości sygnalow nie są rowne.")
        for i in range(len(self.data)):
            self.data[i] *= second_signal.data[i]
        return self.generate_bar_chart(), self.generate_chart()

    def divide(self, second_signal):
        if len(self.data) != len(second_signal.data):
            raise ValueError("Dlugości sygnalow nie są rowne.")
        for i in range(len(self.data)):
            self.data[i] /= second_signal.data[i]
        return self.generate_bar_chart(), self.generate_chart()
