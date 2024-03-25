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
from Signal import Signal
from DataGUI import DataGui


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
            3: SinusoidalSignal,
            4: HalfWave,
            5: FullWave,
            6: SquareWave,
            7: SymmetricalSquareWave,
            8: TriangularWave,
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
                params = {
                    self.mapping_line_edit_params[line_edit.objectName()]:
                        int(line_edit.text()) if line_edit.objectName() == "bins_line_edit" else float(line_edit.text())
                    for line_edit in line_edits
                }
                params['signal_type'] = signal_type
                signal = SignalClass(**params)
                title = 'ID: ' + (self.chart_windows.__len__() + 1).__str__()
                values, chart1, chart2 = signal.generate_data()
                self.signals_objects.append(signal)
                self.show_data_window(title, values, signal)
                self.signalsComboBox.addItem((self.chart_windows.__len__()).__str__())
                self.signalsComboBox2.addItem((self.chart_windows.__len__()).__str__())
            else:
                QMessageBox.warning(self, "Warning", "Some fields are empty.")
            return

    def show_data_window(self, title, values, signal):
        data_gui = DataGui(title, values, signal, parent=self)
        data_gui.id = len(self.chart_windows) + 1
        self.chart_windows.append(data_gui)
        data_gui.show()

    def remove_chart_window(self, id):
        if len(self.chart_windows) > 0:
            self.signalsComboBox.removeItem(id)
            self.signalsComboBox2.removeItem(id)
            for i, window in enumerate(self.chart_windows):
                if hasattr(window, 'id') and window.id == id:
                    index_to_remove = i
                    break
            if index_to_remove is not None:
                self.chart_windows.pop(index_to_remove)

    def operation(self):
        if self.signalsComboBox.currentIndex() != 0 and self.signalsComboBox2.currentIndex() != 0:
            signal1 = self.signals_objects[self.signalsComboBox.currentIndex() - 1]
            signal2 = self.signals_objects[self.signalsComboBox2.currentIndex() - 1]
            op_signal_1 = Signal(signal1.t1, signal1.f, signal1.data, signal1.indexes, signal1.type)
            op_signal_2 = Signal(signal2.t1, signal2.f, signal2.data, signal2.indexes, signal2.type)
            if len(signal1.data) != len(signal2.data):
                QMessageBox.warning(self, "Warning", "Sygnaly musza byc tej samej dlugosci.")
                return
            else:
                if self.operationComboBox.currentIndex() == 1:
                    result_signal = op_signal_1.add(op_signal_2)
                elif self.operationComboBox.currentIndex() == 2:
                    result_signal = op_signal_1.subtract(op_signal_2)
                elif self.operationComboBox.currentIndex() == 3:
                    result_signal = op_signal_1.multiply(op_signal_2)
                elif self.operationComboBox.currentIndex() == 4:
                    result_signal = op_signal_1.divide(op_signal_2)
                values, chart1, chart2 = result_signal.generate_data()
                title = 'ID: ' + (self.chart_windows.__len__() + 1).__str__()
                self.signalsComboBox.addItem((self.chart_windows.__len__() + 1).__str__())
                self.signalsComboBox2.addItem((self.chart_windows.__len__() + 1).__str__())
                self.show_data_window(title, None, result_signal)
                self.signals_objects.append(result_signal)
        else:
            QMessageBox.warning(self, "Warning", "Trzeba wybrac dwa sygnaly.")

    def read_from_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Binary files (*.bin)")
        if fname:
            try:
                signal = Signal.load_from_binary_file(fname[0])
                title = 'ID: ' + (self.chart_windows.__len__() + 1).__str__()
                self.show_data_window(title, None, signal)
                self.signals_objects.append(signal)
                self.signalsComboBox.addItem((self.chart_windows.__len__()).__str__())
                self.signalsComboBox2.addItem((self.chart_windows.__len__()).__str__())
            except Exception as e:
                print("Error reading file:", e)
