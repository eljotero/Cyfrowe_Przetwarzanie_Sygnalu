import numpy as np


class LowPassFilter:

    def __init__(self, Fp, f, M):
        self.M = M
        self.f = f
        self.Fp = Fp

    def filter(self):
        result = []
        K = self.f / self.Fp
        center = int((self.M - 1) / 2)

        for n in range(0, int(self.M), 1):
            if n == center:
                factor = 2.0 / K
            else:
                factor = np.sin(2 * np.pi * (n - center) / K) / (np.pi * (n - center))
            window_value = 0.53836 - 0.46164 * (np.cos(2 * np.pi * n / self.M))
            factor *= window_value
            result.append(factor)

        return result

    def argument(self, i):
        return i * (self.M / (len(self.filter()) - 1))

    def generate_data(self):
        import matplotlib.pyplot as plt
        y_values = self.filter()
        x_values = [self.argument(i) for i in range(len(y_values))]
        plt.clf()
        plt.scatter(x_values, y_values)
        plt.savefig('chart.png')
        return None, plt, None
