from matplotlib import pyplot as plt

from DiscreteSignal import DiscreteSignal


class UnitImpulse(DiscreteSignal):
    def __init__(self, A, ns, n1, l, f, bins=None):
        super().__init__(A, f, n1, l, bins=bins)
        self.l = l
        self.f = f
        self.ns = ns
        self.n1 = n1

    def generate_data(self):
        for i in range(self.l * self.f):
            t = self.n1 + i / self.f
            if t == self.ns:
                self.data.append(1)
            else:
                self.data.append(0)
            self.indexes.append(t)
        self.generate_chart()
        self.generate_bar_chart()

    def generate_chart(self):
        plt.scatter(self.indexes, self.data)
        plt.show()

    def generate_bar_chart(self):
        plt.hist(self.data, bins=self.bins)
        plt.show()
