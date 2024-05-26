from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea
from qtpy import uic

from Sensor import Sensor


class AnalysisGUI(QMainWindow):
    def __init__(self):
        super(AnalysisGUI, self).__init__()
        uic.loadUi('analysis.ui', self)
        self.generateButton.clicked.connect(self.generate_probe_signal)
        self.show()

    def generate_probe_signal(self):
        sensor = Sensor(
            float(self.time_unit_line_edit.text()),
            float(self.object_speed_line_edit.text()),
            float(self.signal_speed_line_edit.text()),
            float(self.signal_period_line_edit.text()),
            float(self.sampling_rate_line_edit.text()),
            int(self.buffer_length_line_edit.text()),
            float(self.reporting_period_line_edit.text())
        )
        sensor.generate_and_plot_signals()
        self.display_images()

    def display_images(self):
        label_probe = QLabel(self)
        label_return = QLabel(self)
        label_correlation = QLabel(self)

        pixmap_probe = QPixmap('probe_signal.png').scaled(400, 300)
        pixmap_return = QPixmap('return_signal.png').scaled(400, 300)
        pixmap_correlation = QPixmap('correlation.png').scaled(400, 300)

        label_probe.setPixmap(pixmap_probe)
        label_return.setPixmap(pixmap_return)
        label_correlation.setPixmap(pixmap_correlation)

        layout = QVBoxLayout()
        layout.addWidget(label_probe)
        layout.addWidget(label_return)
        layout.addWidget(label_correlation)

        container = QWidget()
        container.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)

        self.setCentralWidget(container)

    def closeEvent(self, event):
        self.close()
        event.accept()
