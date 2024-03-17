import pickle
import struct

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic

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
from SignalGenerator import SignalGenerator


class DataGui(QMainWindow):
    def __init__(self, title, values, signal):
        super(DataGui, self).__init__()
        uic.loadUi('datagui.ui', self)
        self.setWindowTitle(title)
        label = QLabel(self)
        label2 = QLabel(self)
        pixmap = QPixmap('chart.png')
        pixmap2 = QPixmap('histogram.png')
        label.setPixmap(pixmap)
        label2.setPixmap(pixmap2)
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label2)
        self.avg_val_line_edit = QLabel(self)
        self.avg_abs_value_line_edit = QLabel(self)
        self.avg_power_line_edit = QLabel(self)
        self.var_value_line_edit = QLabel(self)
        self.eff_val_line_edit = QLabel(self)
        form_layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel("Average Value:"))
        layout1.addWidget(self.avg_val_line_edit)
        form_layout.addLayout(layout1)
        layout2 = QHBoxLayout()
        layout2.addWidget(QLabel("Average Absolute Value:"))
        layout2.addWidget(self.avg_abs_value_line_edit)
        form_layout.addLayout(layout2)
        layout3 = QHBoxLayout()
        layout3.addWidget(QLabel("Average Power:"))
        layout3.addWidget(self.avg_power_line_edit)
        form_layout.addLayout(layout3)
        layout4 = QHBoxLayout()
        layout4.addWidget(QLabel("Variance Value:"))
        layout4.addWidget(self.var_value_line_edit)
        form_layout.addLayout(layout4)
        layout5 = QHBoxLayout()
        layout5.addWidget(QLabel("Effective Value:"))
        layout5.addWidget(self.eff_val_line_edit)
        form_layout.addLayout(layout5)
        layout.addLayout(form_layout)
        save_button = QPushButton("Zapisz")
        save_button.clicked.connect(lambda: self.save_file(signal))
        layout.addWidget(save_button)
        self.avg_val_line_edit.setText(str(values[0]))
        self.avg_abs_value_line_edit.setText(str(values[1]))
        self.avg_power_line_edit.setText(str(values[2]))
        self.var_value_line_edit.setText(str(values[3]))
        self.eff_val_line_edit.setText(str(values[4]))
        self.avg_val_line_edit.setStyleSheet("border: 1px solid black;")
        self.avg_abs_value_line_edit.setStyleSheet("border: 1px solid black;")
        self.avg_power_line_edit.setStyleSheet("border: 1px solid black;")
        self.var_value_line_edit.setStyleSheet("border: 1px solid black;")
        self.eff_val_line_edit.setStyleSheet("border: 1px solid black;")
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def save_file(self, signal):
        fname = QFileDialog.getSaveFileName(self, 'Save file', 'c:\\', "Binary files (*.bin)")
        if fname:
            signal.save_to_binary_file(fname[0])


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi('gui.ui', self)
        self.show()
        self.chart_windows = []
        self.signals_objects = []
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.generateButton.clicked.connect(self.generate_data)
        self.operationButton.clicked.connect(self.operation)
        self.readFromFileButton.clicked.connect(self.read_from_file)
        self.combobox_mapping_line_edit = {
            1: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.bins_line_edit],
            2: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.bins_line_edit],
            3: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.T_line_edit,
                self.bins_line_edit],
            4: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.T_line_edit,
                self.bins_line_edit],
            5: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.T_line_edit,
                self.bins_line_edit],
            6: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.T_line_edit,
                self.kw_line_edit, self.bins_line_edit],
            7: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.T_line_edit,
                self.kw_line_edit, self.bins_line_edit],
            8: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.T_line_edit,
                self.kw_line_edit, self.bins_line_edit],
            9: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.ts_line_edit,
                self.bins_line_edit],
            10: [self.a_line_edit, self.ns_line_edit, self.n1_line_edit, self.l_line_edit, self.f_line_edit,
                 self.bins_line_edit],
            11: [self.a_line_edit, self.t1_line_edit, self.d_line_edit, self.f_line_edit, self.p_line_edit,
                 self.bins_line_edit]
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
            "p_line_edit": "p",
            "bins_line_edit": "bins"
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
                signal_type = self.comboBox.currentIndex()
                params = {self.mapping_line_edit_params[line_edit.objectName()]: int(line_edit.text()) for line_edit in
                          line_edits}
                params['signal_type'] = signal_type
                signal = SignalClass(**params)
                title = self.comboBox.currentText()
                title = title + ' id:' + (self.chart_windows.__len__() + 1).__str__()
                values, chart1, chart2 = signal.generate_data()
                self.signals_objects.append(signal)
                self.show_data_window(title, values, signal)
                self.signalsComboBox.addItem((self.chart_windows.__len__()).__str__())
                self.signalsComboBox2.addItem((self.chart_windows.__len__()).__str__())
            else:
                QMessageBox.warning(self, "Warning", "Some fields are empty.")
            return

    def show_data_window(self, title, values, signal):
        self.data_gui = DataGui(title, values, signal)
        self.data_gui.show()
        self.chart_windows.append(self.data_gui)

    def operation(self):
        if self.signalsComboBox.currentIndex() != 0 and self.signalsComboBox2.currentIndex() != 0:
            signal1 = self.signals_objects[self.signalsComboBox.currentIndex() - 1]
            signal2 = self.signals_objects[self.signalsComboBox2.currentIndex() - 1]
            if signal1.data.__len__() != signal2.data.__len__():
                QMessageBox.warning(self, "Warning", "Signals have different length.")
                return
            else:
                if self.operationComboBox.currentIndex() == 0:
                    result_signal = signal1.add(signal2)
                elif self.operationComboBox.currentIndex() == 1:
                    result_signal = signal1.subtract(signal2)
                elif self.operationComboBox.currentIndex() == 2:
                    result_signal = signal1.multiply(signal2)
                elif self.operationComboBox.currentIndex() == 3:
                    result_signal = signal1.divide(signal2)
                title = self.operationComboBox.currentText()
                title = title + ' id:' + (self.chart_windows.__len__() + 1).__str__()
                self.signalsComboBox.addItem((self.chart_windows.__len__() + 1).__str__())
                self.signalsComboBox2.addItem((self.chart_windows.__len__() + 1).__str__())
                self.show_data_window(title)
                self.signals_objects.append(result_signal)

    def read_from_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Binary files (*.bin)")
        if fname:
            try:
                self.signal = SignalGenerator.load_from_binary_file(fname[0])
            except Exception as e:
                print("Error reading file:", e)


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == '__main__':
    main()
