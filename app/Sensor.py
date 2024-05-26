import threading
import time

import numpy as np
from matplotlib import pyplot as plt


class Sensor:
    def __init__(self, time_unit, object_speed, signal_speed, signal_period, sampling_rate, buffer_length,
                 reporting_period):
        self.time_unit = time_unit
        self.object_speed = object_speed
        self.signal_speed = signal_speed
        self.signal_period = signal_period
        self.sampling_rate = sampling_rate
        self.buffer_length = buffer_length
        self.reporting_period = reporting_period
        self.probe_signal_buffer = np.zeros(buffer_length)
        self.return_signal_buffer = np.zeros(buffer_length)
        self.distance = 0

    def generate_probe_signal(self):
        t = np.arange(self.buffer_length)
        self.probe_signal_buffer = np.sin(2 * np.pi * t / self.signal_period) + np.sign(
            np.sin(2 * np.pi * t / self.signal_period))

    def simulate_reflection(self):
        distance = self.object_speed * self.time_unit
        delay_samples = int((2 * distance / self.signal_speed) * self.sampling_rate)
        self.return_signal_buffer = np.roll(self.probe_signal_buffer, delay_samples)

    def sample_signals(self):
        self.probe_signal_buffer = self.probe_signal_buffer[:self.buffer_length]
        self.return_signal_buffer = self.return_signal_buffer[:self.buffer_length]

    def calculate_distance(self):
        correlation = np.correlate(self.probe_signal_buffer, self.return_signal_buffer, mode='full')
        shift = np.argmax(correlation) - len(self.probe_signal_buffer) + 1
        self.distance = (shift * self.signal_speed * self.time_unit) / 2

    def report_distance(self):
        start_time = time.time()
        while time.time() - start_time < self.reporting_period:
            print(f"Odległość: {self.distance}")
            time.sleep(self.time_unit)

    def plot_probe_signal(self):
        plt.clf()
        plt.plot(self.probe_signal_buffer)
        plt.title('Probe Signal')
        plt.savefig('probe_signal.png')
        return plt

    def plot_return_signal(self):
        plt.clf()
        plt.plot(self.return_signal_buffer)
        plt.title('Return Signal')
        plt.savefig('return_signal.png')
        return plt

    def plot_correlation(self):
        correlation = np.correlate(self.probe_signal_buffer, self.return_signal_buffer, mode='full')
        plt.clf()
        plt.plot(correlation)
        plt.title('Correlation')
        plt.savefig('correlation.png')
        return plt

    def generate_and_plot_signals(self):
        def run_in_background():
            start_time = time.time()
            while time.time() - start_time < self.reporting_period:
                self.generate_probe_signal()
                self.simulate_reflection()
                self.sample_signals()
                self.calculate_distance()
                self.report_distance()
        thread = threading.Thread(target=run_in_background)
        thread.start()
        return self.plot_probe_signal(), self.plot_return_signal(), self.plot_correlation()