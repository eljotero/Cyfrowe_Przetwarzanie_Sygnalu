from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout
from qtpy import uic

from Sensor import Sensor


class AnalysisGUI(QMainWindow):

    def __init__(self):
        super(AnalysisGUI, self).__init__()
        uic.loadUi('analysis.ui', self)
        self.show()
        self.generateButton.clicked.connect(self.generate_probe_signal)

    def generate_probe_signal(self):
        sensor = Sensor(float(self.time_unit_line_edit.text()), float(self.object_speed_line_edit.text()),
                        float(self.signal_speed_line_edit.text()), float(self.signal_period_line_edit.text()),
                        float(self.sampling_rate_line_edit.text()), int(self.buffer_length_line_edit.text()),
                        float(self.reporting_period_line_edit.text()))
        sensor.generate_and_plot_signals()
        self.display_images()

    def display_images(self):
        label = QLabel(self)
        label2 = QLabel(self)
        label3 = QLabel(self)
        pixmap = QPixmap('probe_signal.png')
        pixmap2 = QPixmap('return_signal.png')
        pixmap3 = QPixmap('correlation.png')
        label.setPixmap(pixmap)
        label2.setPixmap(pixmap2)
        label3.setPixmap(pixmap3)
        label.show()
        label2.show()
        label3.show()
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label2)
        layout.addWidget(label3)
        self.setLayout(layout)
