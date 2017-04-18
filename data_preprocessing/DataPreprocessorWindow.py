from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import pandas as pd
from ColumnWidget import ColumnWidget

class DataPreprocessorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data preprocessor")

        self.data = pd.read_csv("train.csv")
        layout = QGridLayout()
        for i, col in enumerate(self.data.columns):
            layout.addWidget(ColumnWidget(self.data[col]), i // 2, i % 2)
        widget = QWidget()
        widget.setLayout(layout)
        widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        area = QScrollArea()
        area.setWidget(widget)
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        area.setWidgetResizable(True)
        self.setCentralWidget(area)
