import struct

import numpy as np
from matplotlib import pyplot as plt

from SampledSignal import SampledSignal


class Signal:
    def __init__(self, t1, f, data, indexes, type=None, id=None):
        self.t1 = t1
        self.f = f
        if type is None:
            self.type = "float"
        else:
            self.type = type
        self.data = data
        self.indexes = indexes
        self.id = id

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
        result_signal = Signal(self.t1, self.f, self.data, self.indexes)
        for i in range(len(self.data)):
            result_signal.data[i] = self.data[i] + second_signal.data[i]
        return result_signal

    def subtract(self, second_signal):
        if len(self.data) != len(second_signal.data):
            raise ValueError("Dlugosci sygnalow nie są rowne.")
        result_signal = Signal(self.t1, self.f, self.data, self.indexes)
        for i in range(len(self.data)):
            result_signal.data[i] = self.data[i] - second_signal.data[i]
        return result_signal

    def multiply(self, second_signal):
        if len(self.data) != len(second_signal.data):
            raise ValueError("Dlugosci sygnalow nie są rowne.")
        result_signal = Signal(self.t1, self.f, self.data, self.indexes)
        for i in range(len(self.data)):
            result_signal.data[i] = self.data[i] * second_signal.data[i]
        return result_signal

    def divide(self, second_signal):
        if len(self.data) != len(second_signal.data):
            raise ValueError("Dlugosci sygnalow nie są rowne.")
        result_signal = Signal(self.t1, self.f, self.data, self.indexes)
        for i in range(len(self.data)):
            result_signal.data[i] = self.data[i] / second_signal.data[i]
        return result_signal

    def sample(self, rate, id):
        new_data_x = []
        new_data_y = []
        jump = 1 / rate
        duration = self.indexes[-1] - self.indexes[0]
        samples = int(duration * rate) + 1
        t = 0
        for i in range(samples):
            new_data_x.append(t)
            index = min(round(t * self.f), len(self.data) - 1)
            new_data_y.append(self.data[index])
            t += jump
        return SampledSignal(new_data_y, new_data_x, len(self.data), id, rate, self.indexes[-1])

    def quantize_uniform_truncation(data, indexes, num_levels):
        data_min = min(data)
        data_max = max(data)
        delta = (data_max - data_min) / num_levels
        quantized_data = [np.floor((i - data_min) / delta) * delta + data_min for i in data]
        return Signal(None, None, quantized_data, indexes, None)

    def quantize_uniform_rounding(data, indexes, num_levels):
        data_min = min(data)
        data_max = max(data)
        delta = (data_max - data_min) / num_levels
        quantized_data = [round((i - data_min) / delta) * delta + data_min for i in data]
        return Signal(None, None, quantized_data, indexes, None)

    def generate_data(self, case):
        if case == 1:
            return None, self.generate_quantize_chart(), self.generate_bar_chart()
        if case is None:
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

    def compare_signals(self, reconstructed_signal, case):
        plt.clf()
        plt.plot(self.indexes, self.data, label='Original signal')
        if case == 1:
            plt.step(reconstructed_signal.indexes, reconstructed_signal.data, label='Reconstructed signal', where='post')
        if case == 2:
            plt.step(reconstructed_signal.indexes, reconstructed_signal.data, label='Quantized signal', where='post')
        if case == 3:
            plt.plot(reconstructed_signal.indexes, reconstructed_signal.data, label='Reconstructed signal')
        plt.legend()
        plt.savefig('comparison_chart.png')
        original_signal = np.array(self.data)
        reconstructed_signal = np.array(reconstructed_signal.data)
        mse = np.mean((original_signal - reconstructed_signal) ** 2)
        signal_power = np.sum(original_signal ** 2)
        noise_power = np.sum((original_signal - reconstructed_signal) ** 2)
        snr = 10 * np.log10(signal_power / noise_power)
        peak_signal = np.max(original_signal)
        psnr = 20 * np.log10(peak_signal / np.sqrt(mse))
        md = np.max(np.abs(original_signal - reconstructed_signal))
        enob = (snr - 1.76) / 6.02
        return [mse, snr, psnr, md, enob]

    def generate_quantize_chart(self):
        plt.clf()
        plt.step(self.indexes, self.data, label='Original signal')
        plt.savefig('chart.png')
        return plt

    def convolve(self, second_signal, id):
        M = len(self.data)
        N = len(second_signal.data)
        result_data_length = M + N - 1
        result_indexes = [i / self.f for i in range(result_data_length)]
        result_signal = SampledSignal([0] * result_data_length, result_indexes, result_data_length, id, self.f,
                                      end_time=self.indexes[-1])
        for i in range(0, result_data_length):
            sum = 0.0
            for k in range(0, N):
                if i - k >= 0 and i - k < M:
                    sum += self.data[i - k] * second_signal.data[k]
            result_signal.data[i] = sum
        return result_signal

    def direct_correlation(self, second_signal):
        M = len(self.data)
        N = len(second_signal.data)
        result_data_length = M + N - 1
        result_indexes = [i / self.f for i in range(result_data_length)]
        result_signal = SampledSignal([0] * (M + N - 1), result_indexes, M + N - 1, id=self.id, f=self.f,
                                      end_time=self.indexes[-1])

        for i in range(M + N - 1):
            i = i - (N - 1)
            start_k = max(0, i)
            end_k = min(M, N + i)
            for k in range(start_k, end_k):
                result_signal.data[i + N - 1] += self.data[k] * second_signal.data[k - i]
        return result_signal

    def convolution_correlation(self, second_signal):
        reversed_second_signal = Signal(second_signal.t1, second_signal.f, second_signal.data[::-1],
                                        second_signal.indexes)
        return self.convolve(reversed_second_signal, self.id)
