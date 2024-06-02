import numpy as np

from Continuous.SinusoidalSignal import SinusoidalSignal
from Continuous.SymmetricalSquareWave import SymmetricalSquareWave
from Signal import Signal


class Sensor:
    def __init__(self, time_unit, object_speed, signal_speed, signal_period, sampling_rate, buffer_length,
                 reporting_period, total_time):
        self.time_unit = time_unit
        self.object_speed = object_speed
        self.signal_speed = signal_speed
        self.signal_period = signal_period
        self.sampling_rate = sampling_rate
        self.buffer_length = buffer_length
        self.reporting_period = reporting_period
        self.distance = 0
        self.final_signal = None
        self.return_signal = None
        self.total_time = total_time

    def generate_signal(self):
        signal = SinusoidalSignal(1, self.signal_period, 0, 5, self.sampling_rate)
        signal.generate_data()
        signal_1 = Signal(0, self.sampling_rate, signal.data, signal.indexes, None, None)
        signal2 = SymmetricalSquareWave(1, self.signal_period, 0, 5, self.sampling_rate, 0.5)
        signal2.generate_data()
        signal_2 = Signal(0, self.sampling_rate, signal2.data, signal2.indexes, None, None)
        final_signal = signal_1.add(signal_2)
        final_signal.generate_data(None)
        final_signal.indexes = final_signal.indexes[:self.buffer_length]
        final_signal.data = final_signal.data[:self.buffer_length]
        self.final_signal = final_signal

    def generate_return_signal(self):
        delay = 2 * self.distance / self.signal_speed
        delay_samples = int(delay * self.sampling_rate)
        echo_data = np.roll(self.final_signal.data, delay_samples)
        self.return_signal = Signal(0, self.sampling_rate, echo_data, self.final_signal.indexes, None, None)

    def simulation(self):
        self.generate_signal()
        reports = []
        for i in range(int(self.total_time / self.reporting_period)):
            report = []
            print("Current distance: ", self.distance)
            self.generate_return_signal()
            correlation_signal = self.return_signal.direct_correlation(self.final_signal)
            right_half = correlation_signal.data[len(correlation_signal.data) // 2:]
            max_index_right_half = np.argmax(right_half)
            time_delay = correlation_signal.indexes[len(correlation_signal.indexes) // 2 + max_index_right_half] - \
                         correlation_signal.indexes[len(correlation_signal.indexes) // 2]
            print("Max index: ", max_index_right_half)
            print("Max value: ", right_half[max_index_right_half])
            print("Time delay: ", round(time_delay, 4))
            calculated_distance = time_delay * self.signal_speed / 2
            print("Calculated distance: ", round(calculated_distance, 4))
            print("Difference: ", round(abs(self.distance - calculated_distance), 6))
            report.append(self.distance)
            report.append(round(calculated_distance, 4))
            report.append(round(abs(self.distance - calculated_distance), 6))
            self.distance += self.object_speed * self.time_unit
            reports.append(report)
            print("\n")
        return reports


# def main():
#     sensor = Sensor(10, 10, 30000, 1, 1000, 1000, 2, 20)
#     sensor.simulation()
#
#
# if __name__ == '__main__':
#     main()