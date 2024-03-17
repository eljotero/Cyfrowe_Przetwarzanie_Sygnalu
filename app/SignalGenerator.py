import struct
import pickle

import numpy as np
from matplotlib import pyplot as plt

from Continuous.FullWave import FullWave
from Continuous.GaussianNoise import GaussianNoise
from Continuous.HalfWave import HalfWave
from Continuous.SinusoidalSignal import SinusoidalSignal
from Continuous.SquareWave import SquareWave
from Continuous.SymmetricalSquareWave import SymmetricalSquareWave
from Continuous.TriangularWave import TriangularWave
from Continuous.UniformNoise import UniformNoise
from Continuous.UnitStep import UnitStep
from Discrete.ImpulseNoise import ImpulseNoise
from Discrete.UnitImpulse import UnitImpulse


class SignalGenerator:
    def __init__(self, A, t1, d, f, bins=None, signal_type=None):
        self.A = A
        self.t1 = t1
        self.d = d
        self.f = f
        self.signal_type = signal_type
        self.data = []
        self.indexes = []
        self.signal_classes = {
            1: UniformNoise,
            2: GaussianNoise,
            3: FullWave,
            4: HalfWave,
            5: SinusoidalSignal,
            6: SquareWave,
            7: TriangularWave,
            8: SymmetricalSquareWave,
            9: UnitStep,
            10: UnitImpulse,
            11: ImpulseNoise
        }
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

    def save_to_binary_file(self, filename):
        with open(filename, 'wb') as file:
            file.write(struct.pack('<i', self.signal_type))
            file.write(struct.pack('<d', self.indexes[0]))
            file.write(struct.pack('<d', self.f))
            file.write(struct.pack('<i', len(self.data)))
            for value in self.data:
                file.write(struct.pack('<d', value))
            file.write(struct.pack('<d', self.A))
            file.write(struct.pack('<d', self.t1))

    @classmethod
    def load_from_binary_file(cls, filename):
        with open(filename, 'rb') as file:
            signal_type = struct.unpack('<i', file.read(4))[0]
            SignalClass = cls.signal_classes[signal_type]
            signal = SignalClass()
            signal.t1 = struct.unpack('<d', file.read(8))[0]
            signal.f = struct.unpack('<d', file.read(8))[0]
            num_samples = struct.unpack('<i', file.read(4))[0]
            signal.data = []
            for _ in range(num_samples):
                value = struct.unpack('<d', file.read(8))[0]
                signal.data.append(value)
            signal.A = struct.unpack('<d', file.read(8))[0]
            signal.t1 = struct.unpack('<d', file.read(8))[0]
        return signal
