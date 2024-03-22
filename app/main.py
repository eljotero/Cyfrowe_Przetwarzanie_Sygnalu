from PyQt5.QtWidgets import *
from MyGUI import MyGUI


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == '__main__':
    main()
