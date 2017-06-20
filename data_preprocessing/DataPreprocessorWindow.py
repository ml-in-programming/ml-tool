from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import pandas as pd
from ColumnWidget import ColumnWidget

class DataPreprocessorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data preprocessor")

        self.data = pd.read_csv(QApplication.arguments()[1])
        self.update()

    def update(self):
        layout = QGridLayout()
        for i, col in enumerate(self.data.columns):
            layout.addWidget(ColumnWidget(self.data[col], self.data, self), i // 2, i % 2)
        widget = QWidget()
        widget.setLayout(layout)
        area = QScrollArea()
        area.setWidget(widget)
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        area.setWidgetResizable(True)
        self.setCentralWidget(area)
