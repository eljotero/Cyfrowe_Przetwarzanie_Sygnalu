from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget


class CompareGUI(QMainWindow):
    def __init__(self, title, values, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.id = None
        label = QLabel(self)
        pixmap = QPixmap('comparison_chart.png')
        label.setPixmap(pixmap)
        layout = QHBoxLayout()
        layout.addWidget(label)
        if values is not None:
            self.mse_line_edit = QLabel(self)
            self.snr_line_edit = QLabel(self)
            self.psnr_line_edit = QLabel(self)
            self.md_line_edit = QLabel(self)
            form_layout = QVBoxLayout()
            layout1 = QHBoxLayout()
            layout1.addWidget(QLabel("MSE:"))
            layout1.addWidget(self.mse_line_edit)
            form_layout.addLayout(layout1)
            layout2 = QHBoxLayout()
            layout2.addWidget(QLabel("SNR:"))
            layout2.addWidget(self.snr_line_edit)
            form_layout.addLayout(layout2)
            layout3 = QHBoxLayout()
            layout3.addWidget(QLabel("PSNR:"))
            layout3.addWidget(self.psnr_line_edit)
            form_layout.addLayout(layout3)
            layout4 = QHBoxLayout()
            layout4.addWidget(QLabel("MD:"))
            layout4.addWidget(self.md_line_edit)
            form_layout.addLayout(layout4)
            layout.addLayout(form_layout)
            self.mse_line_edit.setText(str(values[0]))
            self.snr_line_edit.setText(str(values[1]))
            self.psnr_line_edit.setText(str(values[2]))
            self.md_line_edit.setText(str(values[3]))
            self.mse_line_edit.setStyleSheet("border: 1px solid black;")
            self.snr_line_edit.setStyleSheet("border: 1px solid black;")
            self.psnr_line_edit.setStyleSheet("border: 1px solid black;")
            self.md_line_edit.setStyleSheet("border: 1px solid black;")
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.closeEvent = self.closeEvent

    def closeEvent(self, event):
        self.parent().remove_compare_window(self.id)
        event.accept()
