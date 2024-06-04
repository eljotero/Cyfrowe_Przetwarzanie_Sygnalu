from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic


class DataGui(QMainWindow):
    def __init__(self, title, values, signal, parent=None):
        super(DataGui, self).__init__(parent)
        uic.loadUi('datagui.ui', self)
        self.setWindowTitle(title)
        self.id = None
        self.signal = signal
        label = QLabel(self)
        label2 = QLabel(self)
        pixmap = QPixmap('./chart.png')
        pixmap2 = QPixmap('./histogram.png')
        label.setPixmap(pixmap)
        label2.setPixmap(pixmap2)
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label2)
        if values is not None:
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
        save_button = QPushButton("Zapisz")
        save_button.clicked.connect(self.save_file)
        layout.addWidget(save_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.closeEvent = self.closeEvent

    def save_file(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', 'c:\\', "Binary files (*.bin)")
        if fname:
            self.signal.save_to_binary_file(fname[0])

    def closeEvent(self, event):
        self.parent().remove_chart_window(self.id)
        event.accept()
