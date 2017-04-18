#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from DataPreprocessorWindow import DataPreprocessorWindow

def main():
    # See http://pyqt.sourceforge.net/Docs/PyQt5/gotchas.html#crashes-on-exit
    global app
    app = QApplication(sys.argv)

    w = DataPreprocessorWindow()
    w.show()

    app.exec()

if __name__ == "__main__":
    main()
