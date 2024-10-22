from matplotlib import pyplot as plt

from Discrete.DiscreteSignal import DiscreteSignal


class UnitImpulse(DiscreteSignal):
    def __init__(self, A, ns, n1, l, f, bins=None, signal_type=None, id=None):
        super().__init__(A, f, n1, l, bins=bins, signal_type=signal_type, id=id)
        self.l = l
        self.f = f
        self.ns = ns
        self.n1 = n1

    def generate_data(self):
        for i in range(int(self.l * self.f)):
            t = self.n1 + i / self.f
            if i == self.ns:
                self.data.append(self.A)
            else:
                self.data.append(0)
            self.indexes.append(t)
        return self.calculate_values(), self.generate_chart(), self.generate_bar_chart()

    def generate_chart(self):
        plt.clf()
        plt.scatter(self.indexes, self.data)
        plt.savefig('chart.png')
        return plt

    def generate_bar_chart(self):
        plt.clf()
        plt.hist(self.data, bins=self.bins)
        plt.savefig('histogram.png')
        return plt
