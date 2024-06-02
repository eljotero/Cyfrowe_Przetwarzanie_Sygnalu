from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
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
            float(self.reporting_period_line_edit.text()),
            float(self.total_time_line_edit.text())
        )
        reports = sensor.simulation()
        self.show_reports(reports)

    def closeEvent(self, event):
        self.close()
        event.accept()

    def show_reports(self, reports):
        table = QTableWidget()
        table.setRowCount(len(reports))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Distance", "Calculated Distance", "Difference"])
        for i in range(len(reports)):
            for j in range(3):
                item = QTableWidgetItem(str(reports[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, j, item)
        table.resizeColumnsToContents()
        layout = QVBoxLayout()
        layout.addWidget(table)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
