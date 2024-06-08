from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QFileDialog


class TransformGUI(QMainWindow):
    def __init__(self, title, time, signal, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.id = None
        self.signal = signal
        label = QLabel(self)
        pixmap = QPixmap('./complex_chart.png')
        label.setPixmap(pixmap)

        self.time_label = QLabel("Time:", self)
        self.time_line_edit = QLabel(self)
        self.time_line_edit.setText(str(time))
        self.time_line_edit.setStyleSheet("border: 1px solid black;")
        self.time_line_edit.setMinimumHeight(self.time_line_edit.sizeHint().height())
        self.time_line_edit.setMaximumHeight(self.time_line_edit.sizeHint().height())
        main_layout = QHBoxLayout()
        time_layout = QHBoxLayout()
        main_layout.addWidget(label)
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.time_line_edit)

        main_layout.addLayout(time_layout)
        save_button = QPushButton("Zapisz")
        save_button.clicked.connect(self.save)
        main_layout.addWidget(save_button)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.closeEvent = self.closeEvent

    def closeEvent(self, event):
        self.parent().remove_transform_window(self.id)
        event.accept()

    def save(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', 'c:\\', "Binary files (*.bin)")
        if fname:
            self.signal.save_to_binary_file(fname[0])
