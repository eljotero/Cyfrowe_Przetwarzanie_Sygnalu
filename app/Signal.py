import math
import struct
import time

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
            data = [struct.unpack('<d', file.read(8))[0] + 1j * struct.unpack('<d', file.read(8))[0] for _ in
                    range(num_samples)] if type == "complex" else [struct.unpack('<d', file.read(8))[0] for _ in
                                                                   range(num_samples)]
            indexes = np.array([t1 + i / f for i in range(len(data))])
            signal = Signal(t1, f, data, indexes, type)
            signal.generate_data(None)
            return signal

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
                if self.type == "complex":
                    file.write(struct.pack('<d', value.real))
                    file.write(struct.pack('<d', value.imag))
                else:
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
            plt.step(reconstructed_signal.indexes, reconstructed_signal.data, label='Reconstructed signal')
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

    def direct_correlation(self, second_signal, id):
        M = len(self.data)
        N = len(second_signal.data)
        result_data_length = M + N - 1
        result_indexes = [i / self.f for i in range(result_data_length)]
        result_signal = SampledSignal([0] * (M + N - 1), result_indexes, M + N - 1, id=id, f=self.f,
                                      end_time=self.indexes[-1])

        for i in range(M + N - 1):
            i = i - (N - 1)
            start_k = max(0, i)
            end_k = min(M, N + i)
            for k in range(start_k, end_k):
                result_signal.data[i + N - 1] += self.data[k] * second_signal.data[k - i]
        return result_signal

    def convolution_correlation(self, second_signal, id):
        reversed_second_signal = Signal(second_signal.t1, second_signal.f, second_signal.data[::-1],
                                        second_signal.indexes)
        return self.convolve(reversed_second_signal, id)

    def generate_complex_chart(self, mode):
        plt.clf()
        fig, axs = plt.subplots(2)
        if mode == "W1":
            axs[0].plot(self.indexes, [value.real for value in self.data])
            axs[1].plot(self.indexes, [value.imag for value in self.data])
        elif mode == "W2":
            axs[0].plot(self.indexes, [abs(value) for value in self.data])
            axs[1].plot(self.indexes, [np.angle(value) for value in self.data])
        plt.savefig('complex_chart.png')
        return plt

    def dft(self):
        start_time = time.time()
        N = len(self.data)
        X = [0] * N
        for k in range(0, N):
            for n in range(0, N):
                X[k] += self.data[n] * (math.cos(2 * math.pi / N * k * n) - 1j * math.sin(2 * math.pi / N * k * n))
        end_time = time.time()
        return Signal(self.t1, self.f, X, self.indexes, "complex", self.id), end_time - start_time

    def dit_fft(self):
        start_time = time.time()
        N = len(self.data)
        if N <= 1:
            end_time = time.time()
            return Signal(self.t1, self.f, self.data, self.indexes, self.type, self.id), end_time - start_time
        else:
            even_part = Signal(self.t1, self.f, self.data[::2], self.indexes[::2], self.type, self.id)
            odd_part = Signal(self.t1, self.f, self.data[1::2], self.indexes[1::2], self.type, self.id)

            fft_even, _ = even_part.dit_fft()
            fft_odd, _ = odd_part.dit_fft()

            combined = [0] * N
            for i in range(N // 2):
                t = np.exp(-2j * np.pi * i / N) * fft_odd.data[i]
                combined[i] = fft_even.data[i] + t
                combined[i + N // 2] = fft_even.data[i] - t
            end_time = time.time()
            return Signal(self.t1, self.f, combined, self.indexes, "complex", self.id), end_time - start_time

    def wavelet_transform_db4(self):
        start_time = time.time()
        h0 = 0.4829629131445341
        h1 = 0.8365163037378079
        h2 = 0.2241438680420134
        h3 = -0.1294095225512604
        g0 = h3
        g1 = -h2
        g2 = h1
        g3 = -h0

        N = len(self.data)
        if N % 2 != 0:
            raise ValueError("Długość sygnału musi być parzysta dla transformacji falkowej DB4.")

        approx_data = [0] * (N // 2)
        detail_data = [0] * (N // 2)

        for i in range(N // 2):
            approx_data[i] = h0 * self.data[2 * i] + h1 * self.data[2 * i + 1] + h2 * self.data[(2 * i + 2) % N] + h3 * \
                             self.data[(2 * i + 3) % N]
            detail_data[i] = g0 * self.data[2 * i] + g1 * self.data[2 * i + 1] + g2 * self.data[(2 * i + 2) % N] + g3 * \
                             self.data[(2 * i + 3) % N]

        approx_indexes = self.indexes[::2]
        detail_indexes = self.indexes[::2]

        approx = Signal(self.t1, self.f, approx_data, approx_indexes, self.type, self.id)
        detail = Signal(self.t1, self.f, detail_data, detail_indexes, self.type, self.id)
        end_time = time.time()
        return approx, detail, end_time - start_time

    def generate_charts(self):
        plt.clf()
        fig, axs = plt.subplots(2, 2)
        frequencies = np.fft.fftfreq(len(self.data), 1 / self.f)
        positive_freq_indices = frequencies >= 0
        frequencies = frequencies[positive_freq_indices]
        data = np.array(self.data)[positive_freq_indices]
        axs[0, 0].plot(frequencies, [value.real for value in data])
        axs[0, 0].set_title('Część rzeczywista amplitudy')
        axs[0, 1].plot(frequencies, [value.imag for value in data])
        axs[0, 1].set_title('Część urojona amplitudy')
        axs[1, 0].plot(frequencies, [abs(value) for value in data])
        axs[1, 0].set_title('Moduł liczby zespolonej')
        axs[1, 1].plot(frequencies, [np.angle(value) for value in data])
        axs[1, 1].set_title('Argument liczby zespolonej')
        plt.tight_layout()
        plt.savefig('complex_chart.png')
        return plt

    def generate_wavelet_charts(self):
        plt.clf()
        approx, detail, time = self.wavelet_transform_db4()
        fig, axs = plt.subplots(2, 1, figsize=(12, 6))
        axs[0].plot(approx.indexes, [value.real for value in approx.data])
        axs[0].set_title('Część rzeczywista sygnału')
        axs[1].plot(detail.indexes, [value.imag for value in detail.data])
        axs[1].set_title('Część urojona sygnału')
        plt.tight_layout()
        plt.savefig('complex_chart.png')
        return plt, time
