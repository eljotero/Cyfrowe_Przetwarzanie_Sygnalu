from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QWidget


class SampledGUI(QMainWindow):
    def __init__(self, title, values, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.id = None
        label = QLabel(self)
        pixmap = QPixmap('./chart.png')
        label.setPixmap(pixmap)
        layout = QHBoxLayout()
        layout.addWidget(label)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.closeEvent = self.closeEvent

    def closeEvent(self, event):
        self.parent().remove_sampled_window(self.id)
        event.accept()
