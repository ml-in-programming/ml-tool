#!/usr/bin/env python3
import sys
import traceback
from PyQt5.QtWidgets import QApplication, QWidget
from DataPreprocessorWindow import DataPreprocessorWindow
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

def main():
    # See "Unhandled Python exceptions" in http://pyqt.sourceforge.net/Docs/PyQt5/incompatibilities.html#pyqt-v5-5
    sys.excepthook = traceback.print_exception

    # See http://pyqt.sourceforge.net/Docs/PyQt5/gotchas.html#crashes-on-exit
    global app
    app = QApplication(sys.argv)

    w = DataPreprocessorWindow()
    w.show()

    app.exec()


if __name__ == "__main__":
    main()
