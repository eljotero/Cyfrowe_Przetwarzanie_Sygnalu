import numpy as np

from .LowPassFilter import LowPassFilter


class BandPassFilter(LowPassFilter):
    def __init__(self, Fp, f, M, window_type, id):
        super().__init__(Fp, f, M, window_type, id)

    def filter(self):
        low_pass_factors = super().filter()
        result = []

        for i in range(len(low_pass_factors)):
            result.append(low_pass_factors[i] * 2 * np.sin(np.pi * i / 2.0))

        return result

