from PyQt5.QtWidgets import QMainWindow
from qtpy import uic


class AnalysisGUI(QMainWindow):

    def __init__(self, title, values, parent=None):
        super().__init__(parent)
        uic.loadUI('analysis.ui', self)
        self.setWindowTitle(title)
        self.id = None
        self.values = values
        self.closeEvent = self.closeEvent
        self.parent = parent
        self.parent.add_analysis_window(self)
        self.show()
