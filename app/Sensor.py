import numpy as np
from Continuous.SinusoidalSignal import SinusoidalSignal
from Continuous.SymmetricalSquareWave import SymmetricalSquareWave
from Signal import Signal


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
        self.real_distance = 1000
        self.final_signal = None
        self.current_distance = 0
        self.total_time = 10

    def probe_signal(self):
        signal = SinusoidalSignal(1, self.signal_period, 0, 5, self.sampling_rate)
        signal_1 = Signal(0, self.sampling_rate, signal.data, signal.indexes, None, None)
        signal.generate_data()
        signal2 = SymmetricalSquareWave(1, self.signal_period, 0, 5, self.sampling_rate, 0.5)
        signal2.generate_data()
        signal_2 = Signal(0, self.sampling_rate, signal2.data, signal2.indexes, None, None)
        final_signal = signal_1.add(signal_2)
        final_signal.generate_data(None)
        final_signal.indexes = final_signal.indexes[:self.buffer_length]
        final_signal.data = final_signal.data[:self.buffer_length]
        self.final_signal = final_signal
        self.probe_signal_buffer = final_signal.data

    def return_signal(self):
        delay = 2 * self.real_distance / self.signal_speed
        delay_samples = int(delay * self.sampling_rate)
        delayed_data = np.roll(self.final_signal.data, delay_samples)
        return Signal(0, self.sampling_rate, delayed_data, self.final_signal.indexes, None, None)

    def simulation(self):
        self.probe_signal()
        for i in range(int(self.total_time / self.reporting_period)):
            self.current_distance += self.object_speed * self.time_unit
            print("Current distance: ", self.current_distance)
            return_signal = self.return_signal()
            self.return_signal_buffer = return_signal.data[:self.buffer_length]
            correlation_signal = self.final_signal.direct_correlation(return_signal)
            right_half = correlation_signal.data[len(correlation_signal.data) // 2:]
            max_index_right_half = np.argmax(right_half)
            max_index = len(correlation_signal.data) // 2 + max_index_right_half
            max_value = correlation_signal.data[max_index]
            print("Max value: ", max_value)
            print("Max index: ", max_index)
            time_delay = max_index / self.sampling_rate
            print("Time delay: ", time_delay)
            calculated_distance = time_delay * self.signal_speed / 2
            print("Calculated distance: ", calculated_distance)
            print("Difference: ", abs(self.current_distance - calculated_distance))
            print("\n")


def main():
    sensor = Sensor(1, 100, 100, 1, 1000, 1000, 1)
    sensor.simulation()


if __name__ == '__main__':
    main()
