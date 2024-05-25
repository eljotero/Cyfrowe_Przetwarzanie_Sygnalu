from PyQt5 import uic
from PyQt5.QtWidgets import *

from Continuous.FullWave import FullWave
from Continuous.GaussianNoise import GaussianNoise
from Continuous.HalfWave import HalfWave
from Continuous.SinusoidalSignal import SinusoidalSignal
from Continuous.SquareWave import SquareWave
from Continuous.SymmetricalSquareWave import SymmetricalSquareWave
from Continuous.TriangularWave import TriangularWave
from Continuous.UniformNoise import UniformNoise
from Continuous.UnitStep import UnitStep
from Discrete.ImpulseNoise import ImpulseNoise
from Discrete.UnitImpulse import UnitImpulse
from Filters.BandPassFilter import BandPassFilter
from Filters.HighPassFilter import HighPassFilter
from Filters.LowPassFilter import LowPassFilter
from Signal import Signal
from .CompareGUI import CompareGUI
from .DataGUI import DataGui
from .SampledGUI import SampledGUI


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
        self.analysisButton.clicked.connect(self.analysis)
        self.id = 1
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
                 self.bins_line_edit],
            12: [self.m_line_edit, self.f_line_edit, self.fp_line_edit],
            13: [self.m_line_edit, self.f_line_edit, self.fp_line_edit],
            14: [self.m_line_edit, self.f_line_edit, self.fp_line_edit]
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
            11: ImpulseNoise,
            12: LowPassFilter,
            13: BandPassFilter,
            14: HighPassFilter
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
            "bins_line_edit": "bins",
            "m_line_edit": "M",
            "fp_line_edit": "Fp",
            "windowComboBox": "window"
        }

    def on_combobox_changed(self, index):
        self.disable_all_line_edits()
        self.clear_all_line_edits()
        if index != 0:
            line_edits = self.combobox_mapping_line_edit.get(index, [])
            for line_edit in line_edits:
                line_edit.setEnabled(True)
            if index in [12, 13, 14]:
                self.windowComboBox.setEnabled(True)
            else:
                self.windowComboBox.setEnabled(False)

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
                window_type = self.windowComboBox.currentIndex()
                params = {
                    self.mapping_line_edit_params[line_edit.objectName()]:
                        int(line_edit.text()) if line_edit.objectName() == "bins_line_edit" else float(line_edit.text())
                    for line_edit in line_edits
                }
                params['signal_type'] = signal_type
                if signal_type in [12, 13, 14]:
                    params.pop('signal_type', None)
                    params['window_type'] = window_type
                    if window_type == 0:
                        QMessageBox.warning(self, "Warning", "Window type must be selected.")
                        return
                signal = SignalClass(**params, id=self.id)
                values, chart1, chart2 = signal.generate_data()
                title = 'ID: ' + (self.id).__str__()
                self.signals_objects.append(signal)
                self.signalsComboBox.addItem((self.id).__str__())
                self.signalsComboBox2.addItem((self.id).__str__())
                if signal_type not in [12, 13, 14]:
                    self.samplingComboBox.addItem((self.id).__str__())
                self.show_data_window(title, values, signal)
            else:
                QMessageBox.warning(self, "Warning", "Some fields are empty.")
            return

    def show_data_window(self, title, values, signal):
        data_gui = DataGui(title, values, signal, parent=self)
        data_gui.id = self.id
        self.id += 1
        self.chart_windows.append(data_gui)
        data_gui.show()

    def show_comparison_window(self, title, values):
        compare_gui = CompareGUI(title, values, parent=self)
        compare_gui.id = self.id
        self.id += 1
        self.compare_windows.append(compare_gui)
        compare_gui.show()

    def show_sampled_window(self, title, values):
        sampled_gui = SampledGUI(title, values, parent=self)
        sampled_gui.id = self.id
        self.sampled_windows.append(sampled_gui)
        sampled_gui.show()

    def remove_chart_window(self, id):
        id_str = str(id)
        index1 = self.signalsComboBox.findText(id_str)
        index2 = self.signalsComboBox2.findText(id_str)
        index3 = self.samplingComboBox.findText(id_str)
        if index1 != -1:
            self.signalsComboBox.removeItem(index1)
        if index2 != -1:
            self.signalsComboBox2.removeItem(index2)
        if index3 != -1:
            self.samplingComboBox.removeItem(index3)
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
        signal_to_remove = None
        for signal in self.sampled_signals:
            if signal.id == id:
                signal_to_remove = signal
                break
        if signal_to_remove is not None:
            self.sampled_signals.remove(signal_to_remove)
        if len(self.sampled_windows) > 0:
            index_to_remove = None
            self.quantizeSignalComboBox.removeItem(id)
            self.reconstructionSignalComboBox.removeItem(id)
            self.signalsComboBox.removeItem(id)
            self.signalsComboBox2.removeItem(id)
            for i, window in enumerate(self.sampled_windows):
                if hasattr(window, 'id') and window.id == id:
                    index_to_remove = i
                    break
            if index_to_remove is not None:
                self.sampled_windows.pop(index_to_remove)

    def operation(self):
        if self.signalsComboBox.currentIndex() != 0 and self.signalsComboBox2.currentIndex() != 0:
            signal1 = self.signals_objects[self.signalsComboBox.currentIndex() - 1]
            signal2 = self.signals_objects[self.signalsComboBox2.currentIndex() - 1]
            op_signal_1 = Signal(getattr(signal1, 't1', None),
                                 getattr(signal1, 'f', None),
                                 getattr(signal1, 'data', None),
                                 getattr(signal1, 'indexes', None),
                                 getattr(signal1, 'type', None))

            op_signal_2 = Signal(getattr(signal2, 't1', None),
                                 getattr(signal2, 'f', None),
                                 getattr(signal2, 'data', None),
                                 getattr(signal2, 'indexes', None),
                                 getattr(signal2, 'type', None))
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
                elif self.operationComboBox.currentIndex() == 5:
                    result_signal = op_signal_1.convolve(op_signal_2, self.id)
                    values, chart1, chart2 = result_signal.generate_data()
                    title = 'ID: ' + (self.id).__str__()
                    self.show_sampled_window(title, values)
                    self.signals_objects.append(result_signal)
                    return
                elif self.operationComboBox.currentIndex() == 6:
                    result_signal = op_signal_1.direct_correlation(op_signal_2)
                    values, chart1, chart2 = result_signal.generate_data()
                    title = 'ID: ' + (self.id).__str__()
                    self.show_sampled_window(title, values)
                    self.signals_objects.append(result_signal)
                    return
                elif self.operationComboBox.currentIndex() == 7:
                    result_signal = op_signal_1.convolution_correlation(op_signal_2)
                    values, chart1, chart2 = result_signal.generate_data()
                    title = 'ID: ' + (self.id).__str__()
                    self.show_sampled_window(title, values)
                    self.signals_objects.append(result_signal)
                    return
                values, chart1, chart2 = result_signal.generate_data(None)
                title = 'ID: ' + (self.id).__str__()
                self.signalsComboBox.addItem((self.id).__str__())
                self.signalsComboBox2.addItem((self.id).__str__())
                self.samplingComboBox.addItem((self.id).__str__())
                self.show_data_window(title, None, result_signal)
                self.signals_objects.append(result_signal)
        else:
            QMessageBox.warning(self, "Warning", "Trzeba wybrac dwa sygnaly.")

    def sampling(self):
        if self.samplingComboBox.currentIndex() != 0:
            signal = self.signals_objects[self.samplingComboBox.currentIndex() - 1]
            op_signal = Signal(signal.t1, signal.f, signal.data, signal.indexes, signal.type)
            new_signal = op_signal.sample(float(self.samplingRate_line_edit.text()), id=self.id)
            values, chart1, chart2 = new_signal.generate_data()
            title = 'ID: ' + (self.id).__str__()
            self.show_sampled_window(title, values)
            self.sampled_signals.append(new_signal)
            self.signals_objects.append(new_signal)
            self.signalsComboBox.addItem((self.id).__str__())
            self.signalsComboBox2.addItem((self.id).__str__())
            selected_signal_id = str(int(self.samplingComboBox.currentText()) + 1)
            self.quantizeSignalComboBox.addItem(selected_signal_id)
            self.reconstructionSignalComboBox.addItem(selected_signal_id)
            self.id += 1

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
            title = 'ID: ' + (self.id).__str__()
            self.show_comparison_window(title, values)

    def reconstruct_signal(self):
        if self.reconstructionTypeComboBox.currentIndex() != 0 and self.reconstructionSignalComboBox.currentIndex() != 0:
            signal = self.sampled_signals[self.reconstructionSignalComboBox.currentIndex() - 1]
            if self.reconstructionTypeComboBox.currentIndex() == 1:
                reconstructed_signal = signal.zero_order_hold_reconstruction()
            elif self.reconstructionTypeComboBox.currentIndex() == 2:
                reconstructed_signal = signal.first_order_interpolation_reconstruction()
            elif self.reconstructionTypeComboBox.currentIndex() == 3 and self.neig_line_edit.text() != "":
                reconstructed_signal = signal.sinc_reconstruction(int(self.neig_line_edit.text()))
            original_signal = self.signals_objects[self.samplingComboBox.currentIndex() - 1]
            original_signal_2 = Signal(original_signal.t1, original_signal.f, original_signal.data,
                                       original_signal.indexes, original_signal.type)
            if self.reconstructionTypeComboBox.currentIndex() == 1:
                values = original_signal_2.compare_signals(reconstructed_signal, 1)
            else:
                values = original_signal_2.compare_signals(reconstructed_signal, 3)
            title = 'ID: ' + (self.id).__str__()
            self.show_comparison_window(title, values)
            self.signals_objects.append(reconstructed_signal)

    def read_from_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Binary files (*.bin)")
        if fname:
            try:
                signal = Signal.load_from_binary_file(fname[0])
                title = 'ID: ' + (self.id).__str__()
                self.show_data_window(title, None, signal)
                self.signals_objects.append(signal)
                self.signalsComboBox.addItem((self.chart_windows.__len__()).__str__())
                self.signalsComboBox2.addItem((self.chart_windows.__len__()).__str__())
                self.samplingComboBox.addItem((self.chart_windows.__len__()).__str__())
            except Exception as e:
                print("Error reading file:", e)

    def analysis(self):
        if self.signalsComboBox.currentIndex() != 0:
            signal = self.signals_objects[self.signalsComboBox.currentIndex() - 1]
            signal.analyze_signal()
