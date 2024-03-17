from SignalGenerator import SignalGenerator


class DiscreteSignal(SignalGenerator):
    def calculate_values(self):
        self.avg_value = 1 / (self.data[-1] - self.data[0] + 1) * sum(self.data)
        self.abs_avg_value = 1 / (self.data[-1] - self.data[0] + 1) * sum([abs(x) for x in self.data])
        self.avg_power = 1 / (self.data[-1] - self.data[0] + 1) * sum([x ** 2 for x in self.data])
        self.variance = 1 / (self.data[-1] - self.data[0] + 1) * sum([(x - self.avg_value) ** 2 for x in self.data])
        self.effect_value = self.avg_power ** 0.5
