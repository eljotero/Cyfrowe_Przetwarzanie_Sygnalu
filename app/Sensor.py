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
        t = np.arange(self.buffer_length) / self.sampling_rate
        sinusoidal_signal = 0.8 * np.sin(2 * np.pi * t / (self.signal_period / 2))
        rectangular_signal = 0.6 * (np.sign(
            np.sin(np.pi * t / (self.signal_period / 2))) + 1) / 2
        self.probe_signal_buffer = sinusoidal_signal + rectangular_signal

    def simulate_reflection(self):
        distance = self.object_speed * self.time_unit
        delay_samples = int((2 * distance / self.signal_speed) * self.sampling_rate)
        if delay_samples > len(self.probe_signal_buffer):
            delay_samples = len(self.probe_signal_buffer)
        self.return_signal_buffer = np.roll(self.probe_signal_buffer, delay_samples)

    def sample_signals(self):
        self.probe_signal_buffer = self.probe_signal_buffer[:self.buffer_length]
        self.return_signal_buffer = self.return_signal_buffer[:self.buffer_length]

    def calculate_distance(self):
        correlation_samples = np.correlate(self.probe_signal_buffer, self.return_signal_buffer, mode='full')
        right_half = correlation_samples[int(len(correlation_samples) / 2): len(correlation_samples) - 1]
        max_sample = np.argmax(right_half)
        t_delay = max_sample / self.sampling_rate
        self.distance = round(((t_delay * self.signal_speed) / 2), 6)

    def report_distance(self):
        start_time = time.time()
        while time.time() - start_time < self.reporting_period:
            print(f"Odległość: {self.distance:.2f} m")
            time.sleep(self.time_unit)

    def plot_probe_signal(self):
        plt.clf()
        plt.plot(self.probe_signal_buffer)
        plt.yscale('linear')
        plt.title('Sygnał Sondujący')
        plt.savefig('probe_signal.png')
        return plt

    def plot_return_signal(self):
        plt.clf()
        plt.plot(self.return_signal_buffer)
        plt.title('Sygnał powrotny')
        plt.savefig('return_signal.png')
        return plt

    def plot_correlation(self):
        correlation = np.correlate(self.probe_signal_buffer, self.return_signal_buffer, mode='full')
        plt.clf()
        plt.plot(correlation)
        plt.yscale('linear')
        plt.title('Korelacja sygnałów')
        plt.savefig('correlation.png')
        return plt

    def generate_and_plot_signals(self):
        def run_in_background(self):
            start_time = time.time()
            while time.time() - start_time < self.reporting_period:
                self.generate_probe_signal()
                self.simulate_reflection()
                self.sample_signals()
                self.calculate_distance()
                self.report_distance()

        thread = threading.Thread(target=lambda: run_in_background(self))
        thread.start()
        return self.plot_probe_signal(), self.plot_return_signal(), self.plot_correlation()