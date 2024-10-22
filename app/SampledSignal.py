import os

import numpy as np
from matplotlib import pyplot as plt


class SampledSignal:
    def __init__(self, data, indexes, original_signal_len, id, f, end_time):
        self.data = data
        self.indexes = indexes
        self.bins = 10
        self.original_signal_len = original_signal_len
        self.id = id
        self.f = f
        self.end_time = end_time

    def generate_chart(self):
        plt.clf()
        plt.scatter(self.indexes, self.data)
        if os.path.exists('chart.png'):
            os.remove('chart.png')
        plt.savefig('chart.png')
        return plt

    def generate_bar_chart(self):
        plt.clf()
        plt.hist(self.data, self.bins)
        plt.savefig('histogram.png')
        return plt

    def generate_data(self):
        return None, self.generate_chart(), self.generate_bar_chart()

    def zero_order_hold_reconstruction(self):
        from Signal import Signal
        reconstructed_signal = np.zeros(self.original_signal_len)
        new_indexes = np.linspace(self.indexes[0], self.indexes[-1], num=self.original_signal_len)
        j = 0
        for i in range(self.original_signal_len):
            while j < len(self.indexes) - 1 and new_indexes[i] >= self.indexes[j + 1]:
                j += 1
            reconstructed_signal[i] = self.data[j]
        return Signal(None, None, reconstructed_signal, new_indexes, None)

    def first_order_interpolation_reconstruction(self):
        from Signal import Signal
        new_indexes = np.linspace(self.indexes[0], self.indexes[-1], num=self.original_signal_len)
        reconstructed_data = np.interp(new_indexes, self.indexes, self.data)
        return Signal(None, None, reconstructed_data, new_indexes, None)

    def sinc_reconstruction(self, neigh_value):
        from Signal import Signal
        reconstructed_data = np.zeros(self.original_signal_len)
        new_indexes = np.linspace(self.indexes[0], self.end_time, num=self.original_signal_len)
        for t in range(self.original_signal_len):
            y = 0
            indices = np.argsort(np.abs(self.indexes - new_indexes[t]))[:neigh_value]
            for i in indices:
                delta_t = self.indexes[i] - new_indexes[t]
                if delta_t == 0:
                    y += self.data[i]
                else:
                    y += self.data[i] * np.sinc(delta_t / (1 / self.f))
            reconstructed_data[t] = y
        return Signal(None, None, reconstructed_data, new_indexes, None)
