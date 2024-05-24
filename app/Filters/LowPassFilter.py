import numpy as np


class LowPassFilter:

    def __init__(self, Fp, f, M, window_type):
        self.M = M
        self.f = f
        self.Fp = Fp
        self.window_type = window_type
        self.data = self.filter()

    def rectangular_window(self):
        return 1

    def hamming_window(self, n):
        return 0.53836 - 0.46164 * np.cos(2 * np.pi * n / self.M)

    def hanning_window(self, n):
        return 0.5 - 0.5 * np.cos(2 * np.pi * n / self.M)

    def blackman_window(self, n):
        return 0.42 - 0.5 * np.cos(2 * np.pi * n / self.M) + 0.08 * np.cos(4 * np.pi * n / self.M)

    def filter(self):
        result = []
        K = self.f / self.Fp
        center = int((self.M - 1) / 2)

        for n in range(0, int(self.M), 1):
            if n == center:
                factor = 2.0 / K
            else:
                factor = np.sin(2 * np.pi * (n - center) / K) / (np.pi * (n - center))
            if self.window_type == 1:
                window_value = self.rectangular_window()
            elif self.window_type == 2:
                window_value = self.hamming_window(n)
            elif self.window_type == 3:
                window_value = self.hanning_window(n)
            else:
                window_value = self.blackman_window(n)
            factor *= window_value
            result.append(factor)

        return result

    def argument(self, i, filter_length):
        return i * (self.M / (filter_length - 1))

    def generate_data(self):
        import matplotlib.pyplot as plt
        y_values = self.filter()
        filter_length = len(y_values)
        x_values = [self.argument(i, filter_length) for i in range(filter_length)]
        plt.clf()
        plt.scatter(x_values, y_values)
        plt.savefig('chart.png')
        return None, plt, None
