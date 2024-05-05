from PyQt5 import uic
from PyQt5.QtWidgets import *

from CompareGUI import CompareGUI
from Continuous.FullWave import FullWave
from Continuous.GaussianNoise import GaussianNoise
from Continuous.HalfWave import HalfWave
from Continuous.SinusoidalSignal import SinusoidalSignal
from Continuous.SquareWave import SquareWave
from Continuous.SymmetricalSquareWave import SymmetricalSquareWave
from Continuous.TriangularWave import TriangularWave
from Continuous.UniformNoise import UniformNoise
from Continuous.UnitStep import UnitStep
from DataGUI import DataGui
from Discrete.ImpulseNoise import ImpulseNoise
from Discrete.UnitImpulse import UnitImpulse
from SampledGUI import SampledGUI
from Signal import Signal


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi('gui.ui', self)
        self.show()
        self.chart_windows = []
        self.signals_objects = []
        self.sampled_signals = []
        self.compare_windows = []
        self.sampled_windows = []
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.generateButton.clicked.connect(self.generate_data)
        self.operationButton.clicked.connect(self.operation)
        self.sampleButton.clicked.connect(self.sampling)
        self.quantizeButton.clicked.connect(self.quantize)
        self.reconstructionButton.clicked.connect(self.reconstruct_signal)
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
                        float(line_edit.text()) if line_edit.objectName() == "kw_line_edit" else int(line_edit.text())
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
                self.samplingComboBox.addItem((self.chart_windows.__len__()).__str__())
            else:
                QMessageBox.warning(self, "Warning", "Some fields are empty.")
            return

    def show_data_window(self, title, values, signal):
        data_gui = DataGui(title, values, signal, parent=self)
        data_gui.id = len(self.chart_windows) + 1
        self.chart_windows.append(data_gui)
        data_gui.show()

    def show_comparison_window(self, title, values):
        compare_gui = CompareGUI(title, values, parent=self)
        compare_gui.id = len(self.chart_windows)
        self.compare_windows.append(compare_gui)
        compare_gui.show()

    def show_sampled_window(self, title, values):
        sampled_gui = SampledGUI(title, values, parent=self)
        sampled_gui.id = len(self.sampled_windows)
        self.sampled_windows.append(sampled_gui)
        sampled_gui.show()

    def remove_chart_window(self, id):
        if len(self.chart_windows) > 0:
            self.signalsComboBox.removeItem(id)
            self.signalsComboBox2.removeItem(id)
            self.samplingComboBox.removeItem(id)
            for i, window in enumerate(self.chart_windows):
                if hasattr(window, 'id') and window.id == id:
                    index_to_remove = i
                    break
            if index_to_remove is not None:
                self.chart_windows.pop(index_to_remove)

    def remove_compare_window(self, id):
        if len(self.compare_windows) > 0:
            for i, window in enumerate(self.compare_windows):
                if hasattr(window, 'id') and window.id == id:
                    index_to_remove = i
                    break
            if index_to_remove is not None:
                self.compare_windows.pop(index_to_remove)

    def remove_sampled_window(self, id):
        if len(self.sampled_signals) > 0:
            index_to_remove = None
            self.quantizeSignalComboBox.removeItem(id + 1)
            self.reconstructionSignalComboBox.removeItem(id + 1)
            for i, window in enumerate(self.sampled_signals):
                if hasattr(window, 'id') and window.id == id:
                    index_to_remove = i
                    break
            if index_to_remove is not None:
                self.sampled_signals.pop(index_to_remove)

    def operation(self):
        if self.signalsComboBox.currentIndex() != 0 and self.signalsComboBox2.currentIndex() != 0:
            signal1 = self.signals_objects[self.signalsComboBox.currentIndex() - 1]
            signal2 = self.signals_objects[self.signalsComboBox2.currentIndex() - 1]
            op_signal_1 = Signal(signal1.t1, signal1.f, signal1.data, signal1.indexes, signal1.type)
            op_signal_2 = Signal(signal2.t1, signal2.f, signal2.data, signal2.indexes, signal2.type)
            if signal1.data.__len__() != signal2.data.__len__():
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
                self.samplingComboBox.addItem((self.chart_windows.__len__() + 1).__str__())
                self.show_data_window(title, None, result_signal)
                self.signals_objects.append(result_signal)
        else:
            QMessageBox.warning(self, "Warning", "Trzeba wybrac dwa sygnaly.")

    def sampling(self):
        if self.samplingComboBox.currentIndex() != 0:
            signal = self.signals_objects[self.samplingComboBox.currentIndex() - 1]
            op_signal = Signal(signal.t1, signal.f, signal.data, signal.indexes, signal.type)
            new_signal = op_signal.sample(float(self.samplingRate_line_edit.text()))
            values, chart1, chart2 = new_signal.generate_data()
            title = 'ID: ' + (self.sampled_windows.__len__() + 1).__str__()
            self.show_sampled_window(title, values)
            self.sampled_signals.append(new_signal)
            self.quantizeSignalComboBox.addItem(str(self.samplingComboBox.currentIndex()))
            self.reconstructionSignalComboBox.addItem(str(self.samplingComboBox.currentIndex()))

    def quantize(self):
        if self.quantizeComboBox.currentIndex() != 0 and self.quantizeSignalComboBox.currentIndex() != 0 and float(
                self.num_level_line_edit.text()) != 0:
            signal = self.sampled_signals[self.quantizeSignalComboBox.currentIndex() - 1]
            if self.quantizeComboBox.currentIndex() == 1:
                new_signal = Signal.quantize_uniform_truncation(signal.data, signal.indexes,
                                                                float(self.num_level_line_edit.text()))
            elif self.quantizeComboBox.currentIndex() == 2:
                new_signal = Signal.quantize_uniform_rounding(signal.data, signal.indexes,
                                                              float(self.num_level_line_edit.text()))
            original_signal = self.sampled_signals[self.samplingComboBox.currentIndex() - 1]
            original_signal_2 = Signal(None, None, original_signal.data,
                                       original_signal.indexes, None)
            values = original_signal_2.compare_signals(new_signal, 2)
            title = 'ID: ' + (self.chart_windows.__len__() + 1).__str__()
            self.show_comparison_window(title, values)

    def reconstruct_signal(self):
        if self.reconstructionTypeComboBox.currentIndex() != 0 and self.reconstructionSignalComboBox.currentIndex() != 0:
            signal = self.sampled_signals[self.reconstructionSignalComboBox.currentIndex() - 1]
            if self.reconstructionTypeComboBox.currentIndex() == 1:
                reconstructed_signal = signal.zero_order_hold_reconstruction()
            elif self.reconstructionTypeComboBox.currentIndex() == 2:
                reconstructed_signal = signal.first_order_interpolation_reconstruction()
            elif self.reconstructionTypeComboBox.currentIndex() == 3 and self.sinc_t_line_edit.text() != "":
                reconstructed_signal = signal.sinc_reconstruction(float(self.sinc_t_line_edit.text()))
            original_signal = self.signals_objects[self.samplingComboBox.currentIndex() - 1]
            original_signal_2 = Signal(original_signal.t1, original_signal.f, original_signal.data,
                                       original_signal.indexes, original_signal.type)
            if self.reconstructionTypeComboBox.currentIndex() == 1:
                values = original_signal_2.compare_signals(reconstructed_signal, 1)
            else:
                values = original_signal_2.compare_signals(reconstructed_signal, None)
            title = 'ID: ' + (self.chart_windows.__len__() + 1).__str__()
            self.show_comparison_window(title, values)
            self.signals_objects.append(reconstructed_signal)

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
                self.samplingComboBox.addItem((self.chart_windows.__len__()).__str__())
            except Exception as e:
                print("Error reading file:", e)
