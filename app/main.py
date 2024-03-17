from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.uic.properties import QtWidgets
from matplotlib.backends.backend_template import FigureCanvas

from Continuous.UniformNoise import UniformNoise
from Continuous.GaussianNoise import GaussianNoise
from Continuous.FullWave import FullWave
from Continuous.HalfWave import HalfWave
from Continuous.SinusoidalSignal import SinusoidalSignal
from Continuous.SquareWave import SquareWave
from Continuous.TriangularWave import TriangularWave
from Continuous.SymmetricalSquareWave import SymmetricalSquareWave
from Continuous.UnitStep import UnitStep
from Discrete.UnitImpulse import UnitImpulse
from Discrete.ImpulseNoise import ImpulseNoise


class DataGui(QMainWindow):
    def __init__(self, title):
        super(DataGui, self).__init__()
        uic.loadUi('datagui.ui', self)
        self.setWindowTitle(title)
        label = QLabel(self)
        label2 = QLabel(self)
        pixmap = QPixmap('chart.png')
        pixmap2 = QPixmap('histogram.png')
        label.setPixmap(pixmap)
        label2.setPixmap(pixmap2)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label2)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi('gui.ui', self)
        self.show()
        self.chart_windows = []
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.generateButton.clicked.connect(self.generate_data)
        self.combobox_mapping_line_edit = {
            1: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit],
            2: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit],
            3: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.T_line_edit],
            4: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.T_line_edit],
            5: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.T_line_edit],
            6: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.T_line_edit,
                self.kw_line_edit],
            7: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.T_line_edit,
                self.kw_line_edit],
            8: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.T_line_edit,
                self.kw_line_edit],
            9: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.ts_line_edit],
            10: [self.a_line_edit, self.ns_line_edit, self.n1_line_edit, self.l_line_edit, self.f_line_edit],
            11: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.p_line_edit]
        }
        self.signal_classes = {
            1: UniformNoise,
            2: GaussianNoise,
            3: FullWave,
            4: HalfWave,
            5: SinusoidalSignal,
            6: SquareWave,
            7: TriangularWave,
            8: SymmetricalSquareWave,
            9: UnitStep,
            10: UnitImpulse,
            11: ImpulseNoise
        }

        self.mapping_line_edit_params = {
            "a_line_edit": "A",
            "t1_line_edit": "t1",
            "d_line_edit": "d",
            "f_line_edit": "f",
            "T_line_edit": "T",
            "kw_line_edit": "kw",
            "ns_line_edit": "ns",
            "n1_line_edit": "n1",
            "l_line_edit": "l",
            "ts_line_edit": "ts",
            "p_line_edit": "p"
        }

    def on_combobox_changed(self, index):
        self.disable_all_line_edits()
        self.clear_all_line_edits()
        if index != 0:
            line_edits = self.combobox_mapping_line_edit.get(index, [])
            for line_edit in line_edits:
                line_edit.setEnabled(True)

    def disable_all_line_edits(self):
        for line_edit_list in self.combobox_mapping_line_edit.values():
            for line_edit in line_edit_list:
                line_edit.setEnabled(False)

    def clear_all_line_edits(self):
        for line_edit_list in self.combobox_mapping_line_edit.values():
            for line_edit in line_edit_list:
                line_edit.clear()

    def generate_data(self):
        if self.comboBox.currentIndex() != 0:
            line_edits = self.combobox_mapping_line_edit[self.comboBox.currentIndex()]
            if all([line_edit.text() for line_edit in line_edits]):
                SignalClass = self.signal_classes[self.comboBox.currentIndex()]
                params = {self.mapping_line_edit_params[line_edit.objectName()]: int(line_edit.text()) for line_edit in
                          line_edits}
                signal = SignalClass(**params)
                title = self.comboBox.currentText()
                title = title + ' id:' + (self.chart_windows.__len__() + 1).__str__()
                values, chart1, chart2 = signal.generate_data()
                self.show_data_window(title)
            else:
                QMessageBox.warning(self, "Warning", "Some fields are empty.")
            return

    def show_data_window(self, title):
        self.data_gui = DataGui(title)
        self.data_gui.show()
        self.chart_windows.append(self.data_gui)


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == '__main__':
    main()
