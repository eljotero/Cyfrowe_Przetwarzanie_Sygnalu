from .LowPassFilter import LowPassFilter


class HighPassFilter(LowPassFilter):
    def __init__(self, Fp, f, M):
        super().__init__(Fp, f, M)

    def filter(self):
        low_pass_factors = super().filter()
        result = []

        for i in range(len(low_pass_factors)):
            result.append(low_pass_factors[i] * (1 if i % 2 == 0 else -1))

        return result
